"""
Salesforce Sandbox Configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Salesforce Sandbox Credentials
SF_USERNAME = os.getenv('SF_USERNAME', '')
SF_PASSWORD = os.getenv('SF_PASSWORD', '')
SF_SECURITY_TOKEN = os.getenv('SF_SECURITY_TOKEN', '')

# For sandbox, use 'test'. For production, use 'login'
SF_DOMAIN = os.getenv('SF_DOMAIN', 'test')

# API Version (update as needed)
SF_API_VERSION = '59.0'
