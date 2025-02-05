import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

class XubioAgent:
    def __init__(self, client_id: str, secret_id: str):
        self.client_id = client_id
        self.secret_id = secret_id
        self.base_url = 'https://xubio.com/API/1.1'
        self.token = None
        self.token_expiry = None
        
    @classmethod
    def from_env(cls):
        load_dotenv()
        return cls(
            client_id=os.getenv('XUBIO_CLIENT_ID'),
            secret_id=os.getenv('XUBIO_API_KEY')
        )

    def _get_token(self) -> str:
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.token

        auth = (self.client_id, self.secret_id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post(
            f'{self.base_url}/TokenEndpoint',
            headers=headers,
            data=data,
            auth=auth
        )
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=int(token_data['expires_in']))
        return self.token

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f'{self.base_url}/{endpoint}'
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self._get_token()}'
        }
        
        try:
            response = requests.request(method, url, headers=headers, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                error_data = e.response.json()
                if error_data.get('error') == 'invalid_token':
                    # Token expired, clear it and retry once
                    self.token = None
                    self.token_expiry = None
                    headers['Authorization'] = f'Bearer {self._get_token()}'
                    response = requests.request(method, url, headers=headers, json=data, params=params)
                    response.raise_for_status()
                    return response.json()
            raise

    def list_customers(self) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'clienteBean')

    def get_customer(self, id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'clienteBean/{id}')

    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', 'clienteBean', data=data)

    def get_sales(self) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'facturaVentaBean')

    def create_sale(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', 'facturaVentaBean', data=data)