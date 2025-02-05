import os
from dotenv import load_dotenv

def get_xubio_credentials():
    """Load XUBIO credentials from environment variables"""
    load_dotenv()
    
    required_vars = [
        'XUBIO_API_KEY',
        'XUBIO_CLIENT_ID',
        'XUBIO_USERNAME',
        'XUBIO_TENANT_ID'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
    return {
        'api_key': os.getenv('XUBIO_API_KEY'),
        'tenant_id': os.getenv('XUBIO_TENANT_ID'),
        'client_id': os.getenv('XUBIO_CLIENT_ID'),
        'username': os.getenv('XUBIO_USERNAME')
    }