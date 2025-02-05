import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from .agent import XubioAgent

class TestXubioAgent(unittest.TestCase):
    def setUp(self):
        self.agent = XubioAgent(
            client_id='test_client_id',
            secret_id='test_secret_id'
        )
        
    def test_initialization(self):
        self.assertEqual(self.agent.client_id, 'test_client_id')
        self.assertEqual(self.agent.secret_id, 'test_secret_id')
        self.assertIsNone(self.agent.token)
        self.assertIsNone(self.agent.token_expiry)
        
    @patch('requests.post')
    def test_get_token(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': '3600'
        }
        mock_post.return_value = mock_response
        
        token = self.agent._get_token()
        
        self.assertEqual(token, 'test_token')
        self.assertIsNotNone(self.agent.token_expiry)
        mock_post.assert_called_once()
        
    @patch('requests.post')
    def test_token_reuse(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': '3600'
        }
        mock_post.return_value = mock_response
        
        self.agent._get_token()  # First call
        mock_post.reset_mock()
        self.agent._get_token()  # Second call
        
        mock_post.assert_not_called()  # Should reuse existing token
        
    @patch('requests.request')
    @patch('requests.post')
    def test_list_customers(self, mock_post, mock_request):
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': '3600'
        }
        mock_post.return_value = mock_token_response
        
        mock_customers_response = MagicMock()
        mock_customers_response.json.return_value = [{'id': 1, 'name': 'Test Customer'}]
        mock_request.return_value = mock_customers_response
        
        customers = self.agent.list_customers()
        
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]['name'], 'Test Customer')
        mock_request.assert_called_once()
        
    @patch('requests.request')
    @patch('requests.post')
    def test_token_refresh_on_invalid(self, mock_post, mock_request):
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': '3600'
        }
        mock_post.return_value = mock_token_response
        
        # First request fails with invalid token
        mock_error_response = MagicMock()
        mock_error_response.status_code = 401
        mock_error_response.json.return_value = {'error': 'invalid_token'}
        mock_error = requests.exceptions.HTTPError(response=mock_error_response)
        
        # Second request succeeds
        mock_success_response = MagicMock()
        mock_success_response.json.return_value = [{'id': 1}]
        
        mock_request.side_effect = [mock_error, mock_success_response]
        
        customers = self.agent.list_customers()
        
        self.assertEqual(len(customers), 1)
        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(mock_post.call_count, 2)  # Token refreshed

if __name__ == '__main__':
    unittest.main()