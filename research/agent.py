import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

class XubioAgent:
    def __init__(self, client_id: str, api_key: str, username: str = None, tenant_id: str = None):
        self.client_id = client_id
        self.api_key = api_key
        self.username = username
        self.tenant_id = tenant_id
        self.base_url = 'https://api.xubio.com/v1'
        self.session = requests.Session()
        self.session.headers.update({
            'X-Client-Id': client_id,
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        })
        if username:
            self.session.headers.update({'X-Username': username})
        if tenant_id:
            self.session.headers.update({'X-Tenant-ID': tenant_id})
    
    @classmethod
    def from_env(cls):
        load_dotenv()
        return cls(
            client_id=os.getenv('XUBIO_CLIENT_ID'),
            api_key=os.getenv('XUBIO_API_KEY'),
            username=os.getenv('XUBIO_USERNAME'),
            tenant_id=os.getenv('XUBIO_TENANT_ID')
        )

[rest of the code remains the same...]