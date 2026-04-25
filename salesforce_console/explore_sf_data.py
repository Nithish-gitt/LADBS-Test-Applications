"""
Script to explore Salesforce data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.salesforce_client import SalesforceClient

client = SalesforceClient()
sf = client.connect()

# List common objects and record counts
objects = ['Account', 'Contact', 'Lead', 'Opportunity', 'Case', 'User']
print('\n=== Record Counts ===')
for obj in objects:
    try:
        result = sf.query(f'SELECT COUNT() FROM {obj}')
        print(f'{obj}: {result["totalSize"]} records')
    except Exception as e:
        print(f'{obj}: Not available or no access')

# Sample Account data
print('\n=== Sample Accounts (First 5) ===')
accounts = client.query("SELECT Id, Name, Industry, Type FROM Account LIMIT 5")
for acc in accounts['records']:
    print(f"  - {acc['Name']} | Industry: {acc.get('Industry', 'N/A')} | Type: {acc.get('Type', 'N/A')}")

# Sample Contact data
print('\n=== Sample Contacts (First 5) ===')
contacts = client.query("SELECT Id, Name, Email, Account.Name FROM Contact LIMIT 5")
for con in contacts['records']:
    acc_name = con.get('Account', {}).get('Name', 'N/A') if con.get('Account') else 'N/A'
    print(f"  - {con['Name']} | Email: {con.get('Email', 'N/A')} | Account: {acc_name}")

client.disconnect()
