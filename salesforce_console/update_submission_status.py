"""
Script to update Submission status to Completed for a given Application ID
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.salesforce_client import SalesforceClient

# Initialize client
client = SalesforceClient()
sf = client.connect()

# ============================================
# Get Application ID from user
# ============================================
application_id = input("\nEnter the Application ID: ").strip()

if not application_id:
    print("✗ Error: Application ID is required")
    client.disconnect()
    sys.exit(1)

# ============================================
# Find Submissions for the given Application ID
# ============================================
print(f"\nSearching for Submissions linked to Application: {application_id}")

try:
    # Query submissions related to the application
    # Adjust the field name if your lookup field is different
    application_Id = f"SELECT Id FROM MUSW__Application2__c WHERE Name = '{application_id}'"
    res = sf.query(application_Id)
    AppId = res['records'][0]['Id'] if res['records'] else None
    query = f"""
        SELECT Id, Name, MUSW__Status__c 
        FROM MUSW__Submission__c 
        WHERE MUSW__Application2__c = '{AppId}'
    """
    
    result = sf.query(query)
    submissions = result['records']
    
    if not submissions:
        print(f"✗ No submissions found for Application ID: {application_id}")
        client.disconnect()
        sys.exit(0)
    
    print(f"\n✓ Found {len(submissions)} submission(s):")
    print(f"{'Submission ID':<20} {'Name':<30} {'Current Status'}")
    print("-" * 70)
    
    for sub in submissions:
        print(f"{sub['Id']:<20} {sub.get('Name', 'N/A'):<30} {sub.get('MUSW__Status__c', 'N/A')}")
    
    # ============================================
    # Confirm before updating
    # ============================================
    confirm = input(f"\nUpdate {len(submissions)} submission(s) to 'Completed'? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("✗ Update cancelled")
        client.disconnect()
        sys.exit(0)
    
    # ============================================
    # Update each submission
    # ============================================
    print("\nUpdating submissions...")
    success_count = 0
    error_count = 0
    
    for sub in submissions:
        try:
            sf.MUSW__Submission__c.update(sub['Id'], {
                'MUSW__Status__c': 'Completed'
            })
            print(f"  ✓ Updated: {sub['Id']}")
            success_count += 1
        except Exception as e:
            print(f"  ✗ Failed to update {sub['Id']}: {e}")
            error_count += 1
    
    # ============================================
    # Summary
    # ============================================
    print(f"\n=== Update Summary ===")
    print(f"  Total: {len(submissions)}")
    print(f"  Success: {success_count}")
    print(f"  Failed: {error_count}")
    
    # Verify updates
    if success_count > 0:
        print("\n=== Verification ===")
        verify_result = sf.query(query)
        for sub in verify_result['records']:
            status = sub.get('MUSW__Status__c', 'N/A')
            status_icon = "✓" if status == "Completed" else "✗"
            print(f"  {status_icon} {sub['Id']}: {status}")

except Exception as e:
    print(f"\n✗ Error: {e}")

finally:
    client.disconnect()
