"""
Script to find Permit Application object and list its fields
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.salesforce_client import SalesforceClient

# Initialize client
client = SalesforceClient()
sf = client.connect()

# ============================================
# Search for Permit-related objects
# ============================================
print("\n=== Searching for Permit-related Objects ===")

# Get all objects in the org
all_objects = sf.describe()['sobjects']

# Filter for permit-related objects
permit_objects = [obj for obj in all_objects if 'permit' in obj['name'].lower() or 'permit' in obj['label'].lower()]

if permit_objects:
    print(f"Found {len(permit_objects)} permit-related object(s):\n")
    for obj in permit_objects:
        print(f"  API Name: {obj['name']}")
        print(f"  Label: {obj['label']}")
        print(f"  Createable: {obj['createable']}")
        print("-" * 40)
else:
    print("No permit-related objects found.")
    print("\nListing all custom objects (__c suffix):")
    custom_objects = [obj for obj in all_objects if obj['name'].endswith('__c')]
    for obj in custom_objects[:20]:  # Show first 20
        print(f"  {obj['name']} - {obj['label']}")

client.disconnect()
