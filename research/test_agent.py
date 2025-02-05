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
        mock_post.assert_called_once_with(
            'https://xubio.com/API/1.1/TokenEndpoint',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'grant_type': 'client_credentials'},
            auth=('test_client_id', 'test_secret_id')
        )

    @patch('requests.request')
    @patch.object(XubioAgent, '_get_token')
    def test_list_customers(self, mock_get_token, mock_request):
        mock_get_token.return_value = 'test_token'
        mock_response = MagicMock()
        mock_response.json.return_value = [{'id': 1, 'name': 'Test Customer'}]
        mock_request.return_value = mock_response

        customers = self.agent.list_customers()
        
        self.assertEqual(len(customers), 1)
        mock_request.assert_called_once_with(
            'GET',
            'https://xubio.com/API/1.1/clienteBean',
            headers={
                'Accept': 'application/json',
                'Authorization': 'Bearer test_token'
            },
            json=None,
            params=None
        )

    @patch('requests.request')
    @patch.object(XubioAgent, '_get_token')
    def test_token_refresh_on_expired(self, mock_get_token, mock_request):
        mock_get_token.side_effect = ['old_token', 'new_token']
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'invalid_token'}
        mock_response.raise_for_status.side_effect = [
            requests.exceptions.HTTPError(response=mock_response),
            None
        ]
        mock_request.return_value = mock_response

        try:
            self.agent.list_customers()
        except:
            pass
            
        self.assertEqual(mock_get_token.call_count, 2)

if __name__ == '__main__':
    unittest.main()