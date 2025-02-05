import unittest
from .agent import XubioAgent

class TestXubioIntegration(unittest.TestCase):
    def setUp(self):
        self.agent = XubioAgent.from_env()

    def test_connection(self):
        """Test API connection using credentials"""
        try:
            customers = self.agent.list_customers()
            self.assertIsNotNone(customers)
            print(f"Successfully connected to XUBIO API")
        except Exception as e:
            self.fail(f"Connection failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()