"""
Script to get Permit Application lookup values
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.salesforce_client import SalesforceClient

# Initialize client
client = SalesforceClient()
sf = client.connect()

# ============================================
# First, get available Record Types for Permit Application
# ============================================
print("=== Available Record Types ===")
record_types = sf.query("""
    SELECT Id, Name, DeveloperName 
    FROM RecordType 
    WHERE SObjectType = 'MUSW__Permit_Application__c' AND IsActive = true
""")
for rt in record_types['records']:
    print(f"  {rt['Name']}: {rt['Id']}")

# ============================================
# Get sample Account IDs (for MUSW__Account__c)
# ============================================
print("\n=== Sample Accounts (use one for MUSW__Account__c) ===")
accounts = sf.query("SELECT Id, Name FROM Account LIMIT 5")
for acc in accounts['records']:
    print(f"  {acc['Name']}: {acc['Id']}")

# ============================================
# Get sample Contact IDs (for MUSW__Applicant__c if it's a Contact lookup)
# ============================================
print("\n=== Sample Contacts (use one for MUSW__Applicant__c) ===")
contacts = sf.query("SELECT Id, Name FROM Contact LIMIT 5")
for con in contacts['records']:
    print(f"  {con['Name']}: {con['Id']}")

# ============================================
# Get Use Class picklist values (if it's a picklist)
# ============================================
print("\n=== Use Class Values (for MUSW__Use_Class__c) ===")
try:
    metadata = client.describe_object("MUSW__Permit_Application__c")
    use_class_field = next((f for f in metadata['fields'] if f['name'] == 'MUSW__Use_Class__c'), None)
    if use_class_field and use_class_field.get('picklistValues'):
        for pv in use_class_field['picklistValues']:
            if pv['active']:
                print(f"  {pv['value']}")
    else:
        print("  (Not a picklist - may be a lookup field)")
except Exception as e:
    print(f"  Error: {e}")

# ============================================
# Get Applicant Role picklist values
# ============================================
print("\n=== Applicant Role Values (for LACPS_Applicant_Role__c) ===")
try:
    applicant_role_field = next((f for f in metadata['fields'] if f['name'] == 'LACPS_Applicant_Role__c'), None)
    if applicant_role_field and applicant_role_field.get('picklistValues'):
        for pv in applicant_role_field['picklistValues']:
            if pv['active']:
                print(f"  {pv['value']}")
    else:
        print("  (Not a picklist - may be a lookup or text field)")
except Exception as e:
    print(f"  Error: {e}")

client.disconnect()

print("\n" + "="*60)
print("Copy the IDs/values above and update create_permit_application.py")
print("="*60)
