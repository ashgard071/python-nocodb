import os
import json
import unittest
from PIL import Image
from ..nocodb import NocoDBProject, APIToken, JWTAuthToken
from ..filters import InFilter, EqFilter
from ..infra.requests_client import NocoDBRequestsClient
from datetime import datetime
  
class RequestsClientTest(unittest.TestCase):
  
    
    
    @classmethod
    def setUpClass(cls):
#        cls.client = NocoDBRequestsClient(APIToken(os.environ['NC_TOKEN']), os.environ['NC_HOSTPATH'])
        cls.client = NocoDBRequestsClient(APIToken(os.environ['NC_TOKEN']), os.environ['NC_HOSTPATH'])
        cls.project = NocoDBProject("noco", "WatchNo", "p_i2giuq2epoi5ts")
        cls.table_name = "Logs"

    @classmethod
    def teardownClass(cls):
        print('done')

    def test_all(self):
        fields = {
            'Service name' : {'lt_table': 'Services', 'lt_column': 'Service name', 'lt_value': 'SmartGallery'}, # TOGO get values from spec
#            'Service': [{"Id": 1, "Service name": "SmartGallery"}],
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Level': 'info',
            'Message': 'this is just a test',
            'Host name':'ashgardtest',
            'Host IP': '123.456.789.0',
        }
        table_name = "Logs"
        
        response = self.client.table_row_create(self.project, table_name, fields)
        response2 = self.client.table_row_ltar_update(self.project, table_name, response['Id'], fields)
        print(response2)
        
if __name__ == '__main__':
    print("Run as -> Python unit-test")
    