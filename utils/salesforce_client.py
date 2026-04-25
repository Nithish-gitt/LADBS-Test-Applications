"""
Salesforce Client Utility
Provides connection and common operations for Salesforce Sandbox
"""
from simple_salesforce import Salesforce, SalesforceLogin
from simple_salesforce.exceptions import SalesforceAuthenticationFailed
from config.salesforce_config import (
    SF_USERNAME,
    SF_PASSWORD,
    SF_SECURITY_TOKEN,
    SF_DOMAIN,
    SF_API_VERSION
)


class SalesforceClient:
    """
    A wrapper class for Salesforce API operations.
    Connects to Salesforce Sandbox environment.
    """
    
    def __init__(self, username=None, password=None, security_token=None, domain=None):
        """
        Initialize Salesforce client.
        
        Args:
            username: Salesforce username (defaults to config value)
            password: Salesforce password (defaults to config value)
            security_token: Salesforce security token (defaults to config value)
            domain: 'test' for sandbox, 'login' for production (defaults to config value)
        """
        self.username = username or SF_USERNAME
        self.password = password or SF_PASSWORD
        self.security_token = security_token or SF_SECURITY_TOKEN
        self.domain = domain or SF_DOMAIN
        self.sf = None
        self.session_id = None
        self.instance = None
    
    def connect(self):
        """
        Establish connection to Salesforce Sandbox.
        
        Returns:
            Salesforce: Connected Salesforce instance
            
        Raises:
            SalesforceAuthenticationFailed: If authentication fails
            ValueError: If credentials are missing
        """
        if not all([self.username, self.password, self.security_token]):
            raise ValueError(
                "Missing Salesforce credentials. Please set SF_USERNAME, "
                "SF_PASSWORD, and SF_SECURITY_TOKEN in your .env file."
            )
        
        try:
            self.sf = Salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token,
                domain=self.domain,
                version=SF_API_VERSION
            )
            print(f"✓ Successfully connected to Salesforce Sandbox")
            print(f"  Instance URL: {self.sf.sf_instance}")
            return self.sf
        except SalesforceAuthenticationFailed as e:
            print(f"✗ Authentication failed: {e}")
            raise
    
    def disconnect(self):
        """Close the Salesforce session."""
        if self.sf:
            self.sf = None
            print("✓ Disconnected from Salesforce")
    
    def get_connection(self):
        """
        Get the current Salesforce connection, creating one if needed.
        
        Returns:
            Salesforce: Connected Salesforce instance
        """
        if self.sf is None:
            self.connect()
        return self.sf
    
    # ========== QUERY OPERATIONS ==========
    
    def query(self, soql):
        """
        Execute a SOQL query.
        
        Args:
            soql: SOQL query string
            
        Returns:
            dict: Query results with 'records' key
        """
        sf = self.get_connection()
        return sf.query(soql)
    
    def query_all(self, soql):
        """
        Execute a SOQL query and return all results (handles pagination).
        
        Args:
            soql: SOQL query string
            
        Returns:
            dict: All query results
        """
        sf = self.get_connection()
        return sf.query_all(soql)
    
    # ========== RECORD OPERATIONS ==========
    
    def get_record(self, object_name, record_id, fields=None):
        """
        Get a single record by ID.
        
        Args:
            object_name: Salesforce object API name (e.g., 'Account', 'Contact')
            record_id: Record ID
            fields: List of fields to retrieve (optional)
            
        Returns:
            dict: Record data
        """
        sf = self.get_connection()
        sobject = getattr(sf, object_name)
        if fields:
            return sobject.get(record_id, fields=fields)
        return sobject.get(record_id)
    
    def create_record(self, object_name, data):
        """
        Create a new record.
        
        Args:
            object_name: Salesforce object API name
            data: Dictionary of field values
            
        Returns:
            dict: Result with 'id' of created record
        """
        sf = self.get_connection()
        sobject = getattr(sf, object_name)
        result = sobject.create(data)
        print(f"✓ Created {object_name} record: {result['id']}")
        return result
    
    def update_record(self, object_name, record_id, data):
        """
        Update an existing record.
        
        Args:
            object_name: Salesforce object API name
            record_id: Record ID to update
            data: Dictionary of field values to update
            
        Returns:
            int: HTTP status code (204 for success)
        """
        sf = self.get_connection()
        sobject = getattr(sf, object_name)
        result = sobject.update(record_id, data)
        print(f"✓ Updated {object_name} record: {record_id}")
        return result
    
    def delete_record(self, object_name, record_id):
        """
        Delete a record.
        
        Args:
            object_name: Salesforce object API name
            record_id: Record ID to delete
            
        Returns:
            int: HTTP status code (204 for success)
        """
        sf = self.get_connection()
        sobject = getattr(sf, object_name)
        result = sobject.delete(record_id)
        print(f"✓ Deleted {object_name} record: {record_id}")
        return result
    
    # ========== METADATA OPERATIONS ==========
    
    def describe_object(self, object_name):
        """
        Get metadata for a Salesforce object.
        
        Args:
            object_name: Salesforce object API name
            
        Returns:
            dict: Object metadata including fields, relationships, etc.
        """
        sf = self.get_connection()
        sobject = getattr(sf, object_name)
        return sobject.describe()
    
    def get_object_fields(self, object_name):
        """
        Get list of fields for a Salesforce object.
        
        Args:
            object_name: Salesforce object API name
            
        Returns:
            list: List of field names
        """
        metadata = self.describe_object(object_name)
        return [field['name'] for field in metadata['fields']]
    
    # ========== BULK OPERATIONS ==========
    
    def bulk_create(self, object_name, records):
        """
        Create multiple records using bulk API.
        
        Args:
            object_name: Salesforce object API name
            records: List of dictionaries with field values
            
        Returns:
            list: Results for each record
        """
        sf = self.get_connection()
        sobject = getattr(sf.bulk, object_name)
        return sobject.insert(records)
    
    def bulk_update(self, object_name, records):
        """
        Update multiple records using bulk API.
        
        Args:
            object_name: Salesforce object API name
            records: List of dictionaries with 'Id' and fields to update
            
        Returns:
            list: Results for each record
        """
        sf = self.get_connection()
        sobject = getattr(sf.bulk, object_name)
        return sobject.update(records)


# Singleton instance for easy access
_client = None


def get_salesforce_client():
    """
    Get a singleton Salesforce client instance.
    
    Returns:
        SalesforceClient: Configured client instance
    """
    global _client
    if _client is None:
        _client = SalesforceClient()
    return _client


# Example usage
if __name__ == "__main__":
    # Test connection
    client = SalesforceClient()
    
    try:
        sf = client.connect()
        
        # Example: Query some accounts
        result = client.query("SELECT Id, Name FROM Account LIMIT 5")
        print(f"\nFound {result['totalSize']} accounts:")
        for record in result['records']:
            print(f"  - {record['Name']} ({record['Id']})")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
