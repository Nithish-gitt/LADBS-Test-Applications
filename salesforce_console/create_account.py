"""
Script to create a new Account in Salesforce Sandbox
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.salesforce_client import SalesforceClient

# Initialize client
client = SalesforceClient()
client.connect()

# ============================================
# Define Account data - MODIFY THESE VALUES
# ============================================
account_data = {
    "FirstName": "Test Account",       # Required field
    "LastName": "Demo",                       # Required field
    "Industry": "Technology",                 # Optional
    # "Type": "Prospect",                       # Optional
    "Phone": "+19895964271",                  # Optional
    # "Website": "https://example.com",         # Optional
    "BillingStreet": "123 Main Street",       # Optional
    "BillingCity": "San Francisco",           # Optional
    "BillingState": "CA",                     # Optional
    "BillingPostalCode": "94102",             # Optional
    "BillingCountry": "USA",                  # Optional
    "Description": "Account created via API"  # Optional
}

# ============================================
# Create the Account
# ============================================
try:
    result = client.create_record("Account", account_data)
    print(f"\n✓ Account created successfully!")
    print(f"  Record ID: {result['id']}")
    print(f"  Name: {account_data['Name']}")
    
    # Verify by querying the created record
    created_account = client.get_record("Account", result['id'])
    print(f"\n=== Created Account Details ===")
    print(f"  ID: {created_account['Id']}")
    print(f"  Name: {created_account['Name']}")
    print(f"  Industry: {created_account.get('Industry', 'N/A')}")
    print(f"  Type: {created_account.get('Type', 'N/A')}")
    
except Exception as e:
    print(f"\n✗ Error creating account: {e}")

finally:
    client.disconnect()
