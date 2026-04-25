"""
FastAPI Backend for Salesforce Permit Management
"""
import sys
import os
import logging
import csv
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from utils.salesforce_client import SalesforceClient

# ============================================
# Configure Logging
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================
# CSV File Path for Permit Applications
# ============================================
CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'permit_applications.csv')

app = FastAPI(
    title="Salesforce Permit Management API",
    description="API for managing Salesforce Permit Applications, Submissions, and Reviews",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# Default/Hardcoded Values for Permit Application
# ============================================
DEFAULT_PERMIT_DATA = {
    "RecordTypeId": "012dn000000EVNPAA4",
    "MUSW__Account__c": "001dn00000OE2FVAA1",
    "MUSW__Use_Class__c": "1 or 2 Family Dwelling",
    "LACPS_Applicant_Role__c": "Agent for Owner",
    "MUSW__Object_Record_Type__c": "LACPS_Mechanical",
    "LACPS_Green_Building_Response__c": "None of the above",
}

# Default values for frontend form
DEFAULT_FORM_VALUES = {
    "applicant": "Nithish Vemula",
    "address": "4120 S CAROLINA PL LOS ANGELES CA 90731",
    "permitType": "Mechanical",
    "applicantRole": "Agent for Owner",
    "useClass": "1 or 2 Family Dwelling",
    "RecordTypeId": "012dn000000EVNPAA4",
}


# ============================================
# Request Models
# ============================================
class PermitApplicationRequest(BaseModel):
    applicant: Optional[str] = None
    address: Optional[str] = None
    applicantRole: Optional[str] = None
    useClass: Optional[str] = None
    permitType: Optional[str] = None
    licenseType: Optional[str] = None


class ApplicationNumberRequest(BaseModel):
    applicationNumber: str


# ============================================
# Response Models
# ============================================
class PermitApplicationResponse(BaseModel):
    success: bool
    message: str
    applicationId: Optional[str] = None
    applicationName: Optional[str] = None
    field: Optional[str] = None


class SubmissionResponse(BaseModel):
    success: bool
    message: str
    total: int = 0
    updated: int = 0
    failed: int = 0


class ReviewResponse(BaseModel):
    success: bool
    message: str
    total: int = 0
    updated: int = 0
    failed: int = 0


class PermitTypeOption(BaseModel):
    id: str
    name: str


class PermitTypesResponse(BaseModel):
    success: bool
    permitTypes: List[PermitTypeOption] = []


class PermitHistoryItem(BaseModel):
    permit_type: str
    application_number: str
    timestamp: str


class PermitHistoryResponse(BaseModel):
    success: bool
    applications: List[PermitHistoryItem] = []


# ============================================
# CSV Helper Functions
# ============================================
def add_permit_to_csv(permit_type: str, application_number: str):
    """Add a new permit application record to the CSV file"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)
        
        # Check if file exists and has headers
        file_exists = os.path.exists(CSV_FILE_PATH)
        
        with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['permit_type', 'application_number', 'timestamp'])
            writer.writerow([permit_type, application_number, timestamp])
        
        logger.info(f"Added permit to CSV: {application_number} ({permit_type})")
        return True
    except Exception as e:
        logger.error(f"Failed to add permit to CSV: {str(e)}")
        return False


def get_permits_from_csv() -> List[dict]:
    """Read all permit applications from the CSV file"""
    applications = []
    try:
        if not os.path.exists(CSV_FILE_PATH):
            return applications
        
        with open(CSV_FILE_PATH, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                applications.append({
                    'permit_type': row.get('permit_type', ''),
                    'application_number': row.get('application_number', ''),
                    'timestamp': row.get('timestamp', '')
                })
        
        # Return in reverse order (newest first)
        applications.reverse()
        logger.info(f"Retrieved {len(applications)} permits from CSV")
    except Exception as e:
        logger.error(f"Failed to read permits from CSV: {str(e)}")
    
    return applications


# ============================================
# Helper function to get Salesforce client
# ============================================
def get_sf_client():
    client = SalesforceClient()
    client.connect()
    return client


# ============================================
# Helper functions for lookups
# ============================================
def lookup_applicant_by_name(sf, applicant_name: str) -> str:
    """Look up Contact ID by Name"""
    try:
        query = f"SELECT Id, Name FROM Contact WHERE Name LIKE '%{applicant_name}%' LIMIT 1"
        result = sf.query(query)
        if result['records']:
            return result['records'][0]['Id']
        return None
    except Exception:
        return None


def lookup_address_by_name(sf, address_name: str) -> str:
    """Look up Address ID by Name or Address field"""
    try:
        # Try searching by Name field first
        query = f"SELECT Id, Name FROM MUSW__Address__c WHERE Name LIKE '%{address_name}%' LIMIT 1"
        result = sf.query(query)
        if result['records']:
            return result['records'][0]['Id']
        return None
    except Exception:
        return None


def lookup_permit_type_by_name(sf, permit_type_name: str) -> str:
    """Look up Application Template ID by Name"""
    try:
        query = f"SELECT Id, Name FROM MUSW__Application_Template__c WHERE Name = '{permit_type_name}' LIMIT 1"
        result = sf.query(query)
        if result['records']:
            return result['records'][0]['Id']
        return None
    except Exception:
        return None


def lookup_contractor_license_by_type(sf, license_type: str) -> str:
    """Look up External License ID by License Type"""
    try:
        query = f"SELECT Id, Name, LACPS_License_Types__c FROM LACPS_External_License__c WHERE LACPS_License_Types__c = '{license_type}' LIMIT 1"
        result = sf.query(query)
        if result['records']:
            return result['records'][0]['Id']
        return None
    except Exception as e:
        logger.error(f"Error looking up contractor license: {str(e)}")
        return None


# ============================================
# API Endpoints
# ============================================

@app.get("/")
def root():
    return {"message": "Salesforce Permit Management API", "status": "running"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/permit-types", response_model=PermitTypesResponse)
def get_permit_types():
    """
    Get all available Permit Types (Application Templates) from Salesforce.
    """
    client = None
    try:
        client = get_sf_client()
        sf = client.get_connection()
        
        query = "SELECT Id, Name FROM MUSW__Application_Template__c WHERE MUSW__Active__c = true ORDER BY Name"
        result = sf.query(query)
        
        permit_types = [
            PermitTypeOption(id=record['Id'], name=record['Name'])
            for record in result['records']
        ]
        
        logger.info(f"Fetched {len(permit_types)} permit types successfully")
        return PermitTypesResponse(success=True, permitTypes=permit_types)
        
    except Exception as e:
        logger.error(f"Error fetching permit types: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if client:
            client.disconnect()


@app.post("/api/permit-application", response_model=PermitApplicationResponse)
def create_permit_application(request: PermitApplicationRequest):
    """
    Create a new Permit Application in Salesforce.
    Uses hardcoded values by default, but overrides with user-provided values.
    Looks up Applicant and Address by Name to get their IDs.
    """
    client = None
    try:
        client = get_sf_client()
        sf = client.get_connection()
        
        # Start with default values
        permit_data = DEFAULT_PERMIT_DATA.copy()
        
        # Override with user-provided values if given
        if request.useClass:
            permit_data["MUSW__Use_Class__c"] = request.useClass
        
        if request.applicantRole:
            permit_data["LACPS_Applicant_Role__c"] = request.applicantRole
        
        # Handle License Type for Contractor roles
        if request.licenseType and request.applicantRole in ["Contractor", "Agent for Contractor"]:
            # Set License Classification
            permit_data["LACPS_License_Classification__c"] = request.licenseType
            
            # Lookup Contractor License by License Type
            contractor_license_id = lookup_contractor_license_by_type(sf, request.licenseType)
            if contractor_license_id:
                permit_data["LACPS_Contractor_License__c"] = contractor_license_id
                logger.info(f"Found contractor license ID: {contractor_license_id} for license type: {request.licenseType}")
            else:
                logger.warning(f"No contractor license found for license type: {request.licenseType}")
        
        if request.permitType:
            if request.permitType == "Bldg-Alter/Repair":
                permit_data["RecordTypeId"] = "012dn000000EVNJAA4"  # Bldg-Alter/Repair Template ID
                permit_data["LACPS_BuildingStories__c"] = "12"
                permit_data["LACPS_Waste_Hauler_Exempt__c"] = True
            elif request.permitType == "Electrical" or request.permitType == "EV Charger" or request.permitType == "Solar Water Heater":
                permit_data["RecordTypeId"] = "012dn000000EVNLAA4"  # Electrical Template ID
                permit_data["LACPS_Electrical_Questionnaire_Complete__c"] = True
    
        # Lookup Applicant by Name
        if request.applicant:
            applicant_id = lookup_applicant_by_name(sf, request.applicant)
            if not applicant_id:
                logger.error(f"Invalid Applicant: No contact found with name '{request.applicant}'")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid Applicant: No contact found with name '{request.applicant}'. Please provide a valid applicant name."
                )
            permit_data["MUSW__Applicant__c"] = applicant_id
        
        # Lookup Address by Name
        if request.address:
            address_id = lookup_address_by_name(sf, request.address)
            if not address_id:
                logger.error(f"Invalid Address: No address found matching '{request.address}'")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid Address: No address found matching '{request.address}'. Please provide a valid address."
                )
            permit_data["MUSW__Address__c"] = address_id
        
        # Lookup Permit Type (Application Template) by Name
        if request.permitType:
            permit_type_id = lookup_permit_type_by_name(sf, request.permitType)
            if not permit_type_id:
                logger.error(f"Invalid Permit Type: No application template found with name '{request.permitType}'")
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid Permit Type: No application template found with name '{request.permitType}'. Please select a valid permit type."
                )
            permit_data["MUSW__Application_Template__c"] = permit_type_id
        
        # Create the permit application
        logger.info(f"Creating permit application with data: {permit_data}")
        try:
            result = client.create_record("MUSW__Application2__c", permit_data)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Salesforce error creating permit: {error_msg}")
            
            # Parse Salesforce error to provide user-friendly message
            if "MUSW__Applicant__c" in error_msg or "Applicant" in error_msg:
                logger.error("Error field: Applicant")
                raise HTTPException(status_code=400, detail="Invalid Applicant: Please provide a valid applicant name.")
            elif "MUSW__Address__c" in error_msg or "Address" in error_msg:
                logger.error("Error field: Address")
                raise HTTPException(status_code=400, detail="Invalid Address: Please provide a valid address.")
            elif "MUSW__Application_Template__c" in error_msg or "Template" in error_msg:
                logger.error("Error field: Application Template")
                raise HTTPException(status_code=400, detail="Invalid Permit Type: Please select a valid permit type.")
            elif "MUSW__Use_Class__c" in error_msg or "Use Class" in error_msg:
                logger.error("Error field: Use Class")
                raise HTTPException(status_code=400, detail="Invalid Use Class: Please select a valid use class.")
            elif "LACPS_Applicant_Role__c" in error_msg or "Role" in error_msg:
                logger.error("Error field: Applicant Role")
                raise HTTPException(status_code=400, detail="Invalid Applicant Role: Please select a valid applicant role.")
            elif "RecordTypeId" in error_msg:
                logger.error("Error field: RecordTypeId")
                raise HTTPException(status_code=400, detail="Invalid Record Type: System configuration error. Please contact administrator.")
            elif "REQUIRED_FIELD_MISSING" in error_msg:
                logger.error("Error: Required fields missing")
                raise HTTPException(status_code=400, detail="Missing required fields. Please fill in all required fields.")
            else:
                raise HTTPException(status_code=500, detail=f"Failed to create permit application: {error_msg}")
        
        record_id = result['id']
        
        # Get the application name (auto-generated by Salesforce)
        created_permit = client.get_record("MUSW__Application2__c", record_id)
        application_name = created_permit.get('Name', record_id)
        
        # Add to CSV file for tracking
        permit_type_name = request.permitType or "Unknown"
        add_permit_to_csv(permit_type_name, application_name)
        
        logger.info(f"Permit Application created successfully: {application_name} (ID: {record_id})")
        return PermitApplicationResponse(
            success=True,
            message="Permit Application created successfully!",
            applicationId=record_id,
            applicationName=application_name
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating permit application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if client:
            client.disconnect()


@app.post("/api/complete-submissions", response_model=SubmissionResponse)
def complete_submissions(request: ApplicationNumberRequest):
    """
    Complete all submissions for a given Application Number.
    Updates MUSW__Status__c to 'Completed'.
    """
    client = None
    try:
        client = get_sf_client()
        sf = client.get_connection()
        
        application_number = request.applicationNumber.strip()
        
        if not application_number:
            logger.error("Complete submissions called without application number")
            raise HTTPException(status_code=400, detail="Application Number is required")
        
        logger.info(f"Completing submissions for application: {application_number}")
        
        # Get Application ID from Name
        app_query = f"SELECT Id FROM MUSW__Application2__c WHERE Name = '{application_number}'"
        app_result = sf.query(app_query)
        
        if not app_result['records']:
            logger.error(f"Application not found: {application_number}")
            raise HTTPException(status_code=404, detail=f"Application '{application_number}' not found")
        
        app_id = app_result['records'][0]['Id']
        
        # Find submissions for this application
        query = f"""
            SELECT Id, Name, MUSW__Status__c 
            FROM MUSW__Submission__c 
            WHERE MUSW__Application2__c = '{app_id}'
        """
        result = sf.query(query)
        submissions = result['records']
        
        if not submissions:
            return SubmissionResponse(
                success=True,
                message=f"No submissions found for Application {application_number}",
                total=0,
                updated=0,
                failed=0
            )
        
        # Update each submission
        success_count = 0
        error_count = 0
        
        for sub in submissions:
            try:
                sf.MUSW__Submission__c.update(sub['Id'], {
                    'MUSW__Status__c': 'Completed'
                })
                success_count += 1
            except Exception as sub_error:
                logger.error(f"Failed to update submission {sub['Id']}: {str(sub_error)}")
                error_count += 1
        
        logger.info(f"Submissions completed for {application_number}: {success_count} updated, {error_count} failed")
        return SubmissionResponse(
            success=True,
            message=f"Submissions updated for Application {application_number}",
            total=len(submissions),
            updated=success_count,
            failed=error_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error completing submissions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if client:
            client.disconnect()


@app.post("/api/complete-reviews", response_model=ReviewResponse)
def complete_reviews(request: ApplicationNumberRequest):
    """
    Complete all reviews for a given Application Number.
    Updates MUSW__Status__c to 'Completed' and MUSW__Completed_Action__c to 'Approved'.
    """
    client = None
    try:
        client = get_sf_client()
        sf = client.get_connection()
        
        application_number = request.applicationNumber.strip()
        
        if not application_number:
            logger.error("Complete reviews called without application number")
            raise HTTPException(status_code=400, detail="Application Number is required")
        
        logger.info(f"Completing reviews for application: {application_number}")
        
        # Get Application ID from Name
        app_query = f"SELECT Id FROM MUSW__Application2__c WHERE Name = '{application_number}'"
        app_result = sf.query(app_query)
        
        if not app_result['records']:
            logger.error(f"Application not found: {application_number}")
            raise HTTPException(status_code=404, detail=f"Application '{application_number}' not found")
        
        app_id = app_result['records'][0]['Id']
        
        # Find reviews for this application
        query = f"""
            SELECT Id, Name, MUSW__Status__c, MUSW__Completed_Action__c 
            FROM MUSW__Review__c 
            WHERE MUSW__Application2__c = '{app_id}'
        """
        result = sf.query(query)
        reviews = result['records']
        
        if not reviews:
            return ReviewResponse(
                success=True,
                message=f"No reviews found for Application {application_number}",
                total=0,
                updated=0,
                failed=0
            )
        
        # Update each review
        success_count = 0
        error_count = 0
        
        for rev in reviews:
            try:
                sf.MUSW__Review__c.update(rev['Id'], {
                    'MUSW__Status__c': 'Completed',
                    'MUSW__Completed_Action__c': 'Approved'
                })
                success_count += 1
            except Exception as rev_error:
                logger.error(f"Failed to update review {rev['Id']}: {str(rev_error)}")
                error_count += 1
        
        logger.info(f"Reviews completed for {application_number}: {success_count} updated, {error_count} failed")
        return ReviewResponse(
            success=True,
            message=f"Reviews updated for Application {application_number}",
            total=len(reviews),
            updated=success_count,
            failed=error_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error completing reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if client:
            client.disconnect()


@app.get("/api/default-values")
def get_default_values():
    """
    Get default form values for the frontend.
    """
    logger.info("Returning default form values")
    return DEFAULT_FORM_VALUES


@app.get("/api/permit-history", response_model=PermitHistoryResponse)
def get_permit_history():
    """
    Get all previously created permit applications from the CSV file.
    """
    try:
        applications = get_permits_from_csv()
        history_items = [
            PermitHistoryItem(
                permit_type=app['permit_type'],
                application_number=app['application_number'],
                timestamp=app['timestamp']
            )
            for app in applications
        ]
        return PermitHistoryResponse(success=True, applications=history_items)
    except Exception as e:
        logger.error(f"Error fetching permit history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# Run the server
# ============================================
if __name__ == "__main__":
    import uvicorn
    print("Starting Salesforce Permit Management API...")
    print("API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
