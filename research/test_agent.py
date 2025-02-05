import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from agent import XubioAgent

class TestXubioAgent(unittest.TestCase):
    def setUp(self):
        self.agent = XubioAgent(
            client_id='test_client_id',
            api_key='test_api_key',
            username='test_user',
            tenant_id='test_tenant'
        )
        
    def test_initialization(self):
        self.assertEqual(self.agent.client_id, 'test_client_id')
        self.assertEqual(self.agent.api_key, 'test_api_key')
        self.assertIn('X-Client-Id', self.agent.session.headers)
        self.assertIn('X-Api-Key', self.agent.session.headers)
        
    @patch('requests.Session.request')
    def test_list_customers(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = [{'id': 1, 'name': 'Test Customer'}]
        mock_request.return_value = mock_response
        
        customers = self.agent.list_customers()
        
        mock_request.assert_called_once_with('GET', f'{self.agent.base_url}/customers', json=None)
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]['name'], 'Test Customer')
        
    @patch('requests.Session.request')
    def test_create_invoice(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {'id': 1, 'status': 'created'}
        mock_request.return_value = mock_response
        
        items = [{'product_id': 1, 'quantity': 2, 'price': 100}]
        invoice = self.agent.create_invoice('customer123', items)
        
        mock_request.assert_called_once()
        self.assertEqual(invoice['status'], 'created')
        
    @patch('requests.Session.request')
    def test_get_account_balance(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {'balance': 1000.00}
        mock_request.return_value = mock_response
        
        balance = self.agent.get_account_balance('account123')
        
        mock_request.assert_called_once()
        self.assertEqual(balance['balance'], 1000.00)
        
    @patch('requests.Session.request')
    def test_error_handling(self, mock_request):
        mock_request.side_effect = Exception('API Error')
        
        with self.patch.assertRaises(Exception):
            self.agent.list_customers()
            
    @classmethod
    def from_env_test(cls):
        with patch('os.getenv') as mock_getenv:
            mock_getenv.side_effect = {
                'XUBIO_CLIENT_ID': 'env_client_id',
                'XUBIO_API_KEY': 'env_api_key',
                'XUBIO_USERNAME': 'env_username',
                'XUBIO_TENANT_ID': 'env_tenant_id'
            }.get
            
            agent = XubioAgent.from_env()
            assert agent.client_id == 'env_client_id'
            assert agent.api_key == 'env_api_key'

if __name__ == '__main__':
    unittest.main()