import unittest
import os
from dotenv import load_dotenv
from NexusPythonWrapper import NexusWrapper

class TestNexusWrapper(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.uri = os.getenv('URI')
        self.api_key = os.getenv('APIKEY')
        self.username = os.getenv('NEXUSUSERNAME')
        self.password = os.getenv('PASSWORD')

    def test_authentication_type(self):
        conn = NexusWrapper(
            uri = self.uri,
            authentication_type = 'apikey',
            api_key = self.api_key,
            ssl_verify=False
        )
        self.assertEqual(conn._authentication_type, 'APIKEY')

        conn = NexusWrapper(
            uri=self.uri,
            authentication_type='APIKEY',
            api_key=self.api_key,
            ssl_verify=False
        )
        self.assertEqual(conn._authentication_type, 'APIKEY')

        conn = NexusWrapper(
            uri=self.uri,
            authentication_type='BASIC',
            username=self.username,
            password=self.password,
            ssl_verify=False
        )
        self.assertEqual(conn._authentication_type, 'BASIC')

if __name__ == '__main__':
    unittest.main()