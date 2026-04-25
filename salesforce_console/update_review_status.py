"""
Script to update Review status to Completed and action to Approved for a given Application ID
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
# Find Reviews for the given Application ID
# ============================================
print(f"\nSearching for Reviews linked to Application: {application_id}")

try:
    # Query reviews related to the application
    application_Id = f"SELECT Id FROM MUSW__Application2__c WHERE Name = '{application_id}'"
    res = sf.query(application_Id)
    AppId = res['records'][0]['Id'] if res['records'] else None
    query = f"""
        SELECT Id, Name, MUSW__Status__c, MUSW__Completed_Action__c 
        FROM MUSW__Review__c 
        WHERE MUSW__Application2__c = '{AppId}'
    """
    
    result = sf.query(query)
    reviews = result['records']
    
    if not reviews:
        print(f"✗ No reviews found for Application ID: {application_id}")
        client.disconnect()
        sys.exit(0)
    
    print(f"\n✓ Found {len(reviews)} review(s):")
    print(f"{'Review ID':<20} {'Name':<25} {'Status':<15} {'Completed Action'}")
    print("-" * 85)
    
    for rev in reviews:
        print(f"{rev['Id']:<20} {rev.get('Name', 'N/A'):<25} {rev.get('MUSW__Status__c', 'N/A'):<15} {rev.get('MUSW__Completed_Action__c', 'N/A')}")
    
    # ============================================
    # Confirm before updating
    # ============================================
    print(f"\nUpdates to apply:")
    print(f"  - MUSW__Status__c: Completed")
    print(f"  - MUSW__Completed_Action__c: Approved")
    
    confirm = input(f"\nUpdate {len(reviews)} review(s)? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("✗ Update cancelled")
        client.disconnect()
        sys.exit(0)
    
    # ============================================
    # Update each review
    # ============================================
    print("\nUpdating reviews...")
    success_count = 0
    error_count = 0
    
    for rev in reviews:
        try:
            sf.MUSW__Review__c.update(rev['Id'], {
                'MUSW__Status__c': 'Completed',
                'MUSW__Completed_Action__c': 'Approved'
            })
            print(f"  ✓ Updated: {rev['Id']}")
            success_count += 1
        except Exception as e:
            print(f"  ✗ Failed to update {rev['Id']}: {e}")
            error_count += 1
    
    # ============================================
    # Summary
    # ============================================
    print(f"\n=== Update Summary ===")
    print(f"  Total: {len(reviews)}")
    print(f"  Success: {success_count}")
    print(f"  Failed: {error_count}")
    
    # Verify updates
    if success_count > 0:
        print("\n=== Verification ===")
        verify_result = sf.query(query)
        for rev in verify_result['records']:
            status = rev.get('MUSW__Status__c', 'N/A')
            action = rev.get('MUSW__Completed_Action__c', 'N/A')
            status_icon = "✓" if status == "Completed" and action == "Approved" else "✗"
            print(f"  {status_icon} {rev['Id']}: Status={status}, Action={action}")

except Exception as e:
    print(f"\n✗ Error: {e}")

finally:
    client.disconnect()
