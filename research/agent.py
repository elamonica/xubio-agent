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
        self.base_url = 'https://xubio.com/API/documentation/'
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

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f'{self.base_url}/{endpoint}'
        print(f"Making request to: {url}")  # Debug line
        response = self.session.request(method, url, json=data)
        print(f"Response status: {response.status_code}")  # Debug line
        print(f"Response headers: {response.headers}")  # Debug line
        print(f"Response body: {response.text}")  # Debug line
        response.raise_for_status()
        return response.json()

    def list_customers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'clientes', params)

    def create_invoice(self, customer_id: str, items: List[Dict[str, Any]], date: Optional[str] = None) -> Dict[str, Any]:
        data = {
            'customerId': customer_id,
            'date': date or datetime.now().isoformat(),
            'items': items
        }
        return self._make_request('POST', 'comprobantes', data)

    def get_account_balance(self, account_id: str, date: Optional[str] = None) -> Dict[str, Any]:
        params = {'date': date} if date else None
        return self._make_request('GET', f'cuentas/{account_id}/balance', params)