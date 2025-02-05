import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_load_dotenv

class XubioAgent:
    def __init__(self, api_key: str, tenant_id: str, base_url: str = 'https://api.xubio.com/v1'):
        self.api_key = api_key
        self.tenant_id = tenant_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'X-Tenant-ID': tenant_id,
            'Content-Type': 'application/json'
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f'{self.base_url}/{endpoint}'
        response = self.session.request(method, url, json=data)
        response.raise_for_status()
        return response.json()

    # Invoice Operations
    def create_invoice(self, customer_id: str, items: List[Dict[str, Any]], date: Optional[str] = None) -> Dict[str, Any]:
        """Create a new invoice"""
        data = {
            'customerId': customer_id,
            'date': date or datetime.now().isoformat(),
            'items': items
        }
        return self._make_request('POST', 'invoices', data)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """Get invoice details"""
        return self._make_request('GET', f'invoices/{invoice_id}')

    def list_invoices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List invoices with optional filtering"""
        return self._make_request('GET', 'invoices', params)

    # Customer Operations
    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new customer"""
        return self._make_request('POST', 'customers', data)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details"""
        return self._make_request('GET', f'customers/{customer_id}')

    def list_customers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List customers with optional filtering"""
        return self._make_request('GET', 'customers', params)

    # Account Operations
    def get_chart_of_accounts(self) -> List[Dict[str, Any]]:
        """Get chart of accounts"""
        return self._make_request('GET', 'accounts')

    def get_account_balance(self, account_id: str, date: Optional[str] = None) -> Dict[str, Any]:
        """Get account balance"""
        params = {'date': date} if date else None
        return self._make_request('GET', f'accounts/{account_id}/balance', params)

    # Journal Entry Operations
    def create_journal_entry(self, entries: List[Dict[str, Any]], date: Optional[str] = None) -> Dict[str, Any]:
        """Create a journal entry"""
        data = {
            'date': date or datetime.now().isoformat(),
            'entries': entries
        }
        return self._make_request('POST', 'journal-entries', data)

    def process_command(self, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process natural language commands for XUBIO API"""
        # TODO: Implement NLP processing using OpenAI
        commands = {
            'create_invoice': self.create_invoice,
            'get_invoice': self.get_invoice,
            'list_invoices': self.list_invoices,
            'create_customer': self.create_customer,
            'get_customer': self.get_customer,
            'list_customers': self.list_customers,
            'get_chart_of_accounts': self.get_chart_of_accounts,
            'get_account_balance': self.get_account_balance,
            'create_journal_entry': self.create_journal_entry
        }
        
        # Basic command matching (to be enhanced with NLP)
        for cmd, func in commands.items():
            if cmd in command.lower():
                return func(**(params or {}))
        
        raise ValueError(f"Unknown command: {command}")

# Example usage
if __name__ == "__main__":
    load_dotenv()
    agent = XubioAgent(
        api_key=os.getenv('XUBIO_API_KEY'),
        tenant_id=os.getenv('XUBIO_TENANT_ID')
    )
    
    # Example: List customers
    customers = agent.process_command("list_customers")
    print(json.dumps(customers, indent=2))