import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

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
        data = {
            'customerId': customer_id,
            'date': date or datetime.now().isoformat(),
            'items': items
        }
        return self._make_request('POST', 'invoices', data)

    def get_invoice(self, invoice_id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'invoices/{invoice_id}')

    def list_invoices(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'invoices', params)
    
    def void_invoice(self, invoice_id: str) -> Dict[str, Any]:
        return self._make_request('POST', f'invoices/{invoice_id}/void')

    # Customer Operations
    def create_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', 'customers', data)

    def update_customer(self, customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', f'customers/{customer_id}', data)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'customers/{customer_id}')

    def list_customers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'customers', params)

    def delete_customer(self, customer_id: str) -> None:
        self._make_request('DELETE', f'customers/{customer_id}')

    # Account Operations
    def get_chart_of_accounts(self) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'accounts')

    def create_account(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', 'accounts', data)

    def update_account(self, account_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', f'accounts/{account_id}', data)

    def get_account_balance(self, account_id: str, date: Optional[str] = None) -> Dict[str, Any]:
        params = {'date': date} if date else None
        return self._make_request('GET', f'accounts/{account_id}/balance', params)

    # Journal Entry Operations
    def create_journal_entry(self, entries: List[Dict[str, Any]], date: Optional[str] = None) -> Dict[str, Any]:
        data = {
            'date': date or datetime.now().isoformat(),
            'entries': entries
        }
        return self._make_request('POST', 'journal-entries', data)

    def get_journal_entry(self, entry_id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'journal-entries/{entry_id}')

    def list_journal_entries(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'journal-entries', params)

    # Product Operations
    def create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', 'products', data)

    def get_product(self, product_id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'products/{product_id}')

    def update_product(self, product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', f'products/{product_id}', data)

    def list_products(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'products', params)

    # Purchase Order Operations
    def create_purchase_order(self, supplier_id: str, items: List[Dict[str, Any]], date: Optional[str] = None) -> Dict[str, Any]:
        data = {
            'supplierId': supplier_id,
            'date': date or datetime.now().isoformat(),
            'items': items
        }
        return self._make_request('POST', 'purchase-orders', data)

    def get_purchase_order(self, po_id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'purchase-orders/{po_id}')

    def list_purchase_orders(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'purchase-orders', params)

    # Supplier Operations
    def create_supplier(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('POST', 'suppliers', data)

    def get_supplier(self, supplier_id: str) -> Dict[str, Any]:
        return self._make_request('GET', f'suppliers/{supplier_id}')

    def update_supplier(self, supplier_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._make_request('PUT', f'suppliers/{supplier_id}', data)

    def list_suppliers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'suppliers', params)

    # Tax Operations
    def get_tax_rates(self) -> List[Dict[str, Any]]:
        return self._make_request('GET', 'tax-rates')

    def get_tax_report(self, start_date: str, end_date: str) -> Dict[str, Any]:
        params = {'startDate': start_date, 'endDate': end_date}
        return self._make_request('GET', 'tax-report', params)

    # Financial Reports
    def get_balance_sheet(self, date: str) -> Dict[str, Any]:
        return self._make_request('GET', f'reports/balance-sheet?date={date}')

    def get_income_statement(self, start_date: str, end_date: str) -> Dict[str, Any]:
        params = {'startDate': start_date, 'endDate': end_date}
        return self._make_request('GET', 'reports/income-statement', params)

    def get_cash_flow(self, start_date: str, end_date: str) -> Dict[str, Any]:
        params = {'startDate': start_date, 'endDate': end_date}
        return self._make_request('GET', 'reports/cash-flow', params)

    def get_trial_balance(self, date: str) -> Dict[str, Any]:
        return self._make_request('GET', f'reports/trial-balance?date={date}')

    def process_command(self, command: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process natural language commands for XUBIO API"""
        commands = {
            'create_invoice': self.create_invoice,
            'get_invoice': self.get_invoice,
            'list_invoices': self.list_invoices,
            'void_invoice': self.void_invoice,
            'create_customer': self.create_customer,
            'update_customer': self.update_customer,
            'get_customer': self.get_customer,
            'list_customers': self.list_customers,
            'delete_customer': self.delete_customer,
            'get_chart_of_accounts': self.get_chart_of_accounts,
            'create_account': self.create_account,
            'update_account': self.update_account,
            'get_account_balance': self.get_account_balance,
            'create_journal_entry': self.create_journal_entry,
            'get_journal_entry': self.get_journal_entry,
            'list_journal_entries': self.list_journal_entries,
            'create_product': self.create_product,
            'get_product': self.get_product,
            'update_product': self.update_product,
            'list_products': self.list_products,
            'create_purchase_order': self.create_purchase_order,
            'get_purchase_order': self.get_purchase_order,
            'list_purchase_orders': self.list_purchase_orders,
            'create_supplier': self.create_supplier,
            'get_supplier': self.get_supplier,
            'update_supplier': self.update_supplier,
            'list_suppliers': self.list_suppliers,
            'get_tax_rates': self.get_tax_rates,
            'get_tax_report': self.get_tax_report,
            'get_balance_sheet': self.get_balance_sheet,
            'get_income_statement': self.get_income_statement,
            'get_cash_flow': self.get_cash_flow,
            'get_trial_balance': self.get_trial_balance,
        }
        
        for cmd, func in commands.items():
            if cmd in command.lower():
                return func(**(params or {}))
        
        raise ValueError(f"Unknown command: {command}")

if __name__ == "__main__":
    load_dotenv()
    agent = XubioAgent(
        api_key=os.getenv('XUBIO_API_KEY'),
        tenant_id=os.getenv('XUBIO_TENANT_ID')
    )