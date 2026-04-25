"""
Script to get all fields of a Salesforce object
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.salesforce_client import SalesforceClient

# Initialize client
client = SalesforceClient()
sf = client.connect()

# ============================================
# Find Permit Application object automatically
# ============================================
all_objects = sf.describe()['sobjects']
permit_objects = [obj for obj in all_objects if 'permit' in obj['name'].lower()]

if permit_objects:
    object_name = permit_objects[0]['name']
    print(f"Found Permit object: {object_name}")
else:
    object_name = "Permit_Application__c"  # Fallback - change if needed

# ============================================
# Get object metadata
# ============================================
try:
    metadata = client.describe_object(object_name)
    
    print(f"\n=== {object_name} Object Info ===")
    print(f"Label: {metadata['label']}")
    print(f"Total Fields: {len(metadata['fields'])}")
    print(f"Createable: {metadata['createable']}")
    print(f"Updateable: {metadata['updateable']}")
    
    # Filter to required fields only
    required_fields = [f for f in metadata['fields'] if not f['nillable'] and not f['defaultedOnCreate']]
    
    print(f"\n=== Required Fields ({len(required_fields)}) ===")
    print(f"{'Field Name':<40} {'Type':<15} {'Label'}")
    print("-" * 80)
    
    for field in required_fields:
        print(f"{field['name']:<40} {field['type']:<15} {field['label']}")
    
    # Show all fields
    print(f"\n=== All Fields ({len(metadata['fields'])}) ===")
    print(f"{'Field Name':<40} {'Type':<15} {'Required':<10} {'Label'}")
    print("-" * 100)
    
    for field in metadata['fields']:
        required = "Yes" if not field['nillable'] and not field['defaultedOnCreate'] else "No"
        print(f"{field['name']:<40} {field['type']:<15} {required:<10} {field['label']}")

except Exception as e:
    print(f"\n✗ Error: {e}")

finally:
    client.disconnect()
