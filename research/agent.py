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
        self.base_url = 'https://contabilium.com/api'
        self.session = requests.Session()
        self.session.headers.update({
            'client_id': client_id,
            'client_secret': api_key,
            'Content-Type': 'application/json'
        })

    @classmethod
    def from_env(cls):
        load_dotenv()
        return cls(
            client_id=os.getenv('XUBIO_CLIENT_ID'),
            api_key=os.getenv('XUBIO_API_KEY'),
            username=os.getenv('XUBIO_USERNAME'),
            tenant_id=os.getenv('XUBIO_TENANT_ID')
        )

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f'{self.base_url}/{endpoint}'
        print(f"Making request to: {url}")
        response = self.session.request(method, url, json=data, params=params)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response body: {response.text}")
        response.raise_for_status()
        return response.json()

    def list_customers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'clientes', params=params)

    def create_invoice(self, cliente_id: str, tipo_comprobante: str, fecha: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {
            'cliente': {'id': cliente_id},
            'tipoComprobante': tipo_comprobante,
            'fecha': fecha,
            'items': items
        }
        return self._make_request('POST', 'comprobantes', data=data)

    def get_account_balance(self, account_id: str, fecha_desde: str, fecha_hasta: str) -> Dict[str, Any]:
        params = {
            'fechaDesde': fecha_desde,
            'fechaHasta': fecha_hasta
        }
        return self._make_request('GET', f'cuentas/{account_id}/movimientos', params=params)

    def get_customer(self, id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'clientes/{id}')

    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', 'clientes', data=data)