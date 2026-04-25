"""
Script to create a Permit Application in Salesforce Sandbox
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.salesforce_client import SalesforceClient

# Initialize client
client = SalesforceClient()
client.connect()

# ============================================
# PERMIT APPLICATION DATA - UPDATE THESE VALUES
# Run get_permit_lookup_values.py first to get valid IDs
# ============================================
permit_data = {
    # REQUIRED FIELDS
    "RecordTypeId": "012dn000000EVNPAA4",           # Run get_permit_lookup_values.py to get ID
    "MUSW__Account__c": "001dn00000OE2FVAA1",           # Account ID (18 char)
    "MUSW__Applicant__c": "003dn00000PYEYPAA5",       # Contact/Applicant ID (18 char)
    "MUSW__Use_Class__c": "1 or 2 Family Dwelling",    # Use Class value
    "LACPS_Applicant_Role__c": "Agent for Owner",    # Applicant Role value
    "MUSW__Address__c": "a04dn000006fhK5AAI",  # Address
    "MUSW__Application_Template__c": "a0Fdn0000049i5xEAA",  # Application Template ID (18 char)
    "MUSW__Object_Record_Type__c": "LACPS_Mechanical",  # Object Record Type value
    "LACPS_Green_Building_Response__c": "None of the above",  # Green Building Response value
    # "LACPS_Assessor_s_Identification_Number__c": "2"  # Assessor's ID Number
    # OPTIONAL FIELDS (uncomment and fill as needed)
    # "Name": "Test Permit Application",
    # "MUSW__Description__c": "Test permit created via API",
}

# ============================================
# Create the Permit Application
# ============================================
try:
    result = client.create_record("MUSW__Application2__c", permit_data)
    print(f"\n✓ Permit Application created successfully!")
    print(f"  Record ID: {result['id']}")
    
    # Verify by querying the created record
    created_permit = client.get_record("MUSW__Application2__c", result['id'])
    print(f"\n=== Created Permit Application Details ===")
    print(f"  ID: {created_permit['Id']}")
    print(f"  Name: {created_permit.get('Name', 'N/A')}")
    
except Exception as e:
    print(f"\n✗ Error creating permit application: {e}")

finally:
    client.disconnect()
