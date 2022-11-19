import os
import json
import unittest
from PIL import Image
from ..nocodb import NocoDBProject, APIToken, JWTAuthToken
from ..filters import InFilter, EqFilter
from ..infra.requests_client import NocoDBRequestsClient
  
class RequestsClientTest(unittest.TestCase):
  
    
    
    @classmethod
    def setUpClass(cls):
#        cls.client = NocoDBRequestsClient(APIToken(os.environ['NC_TOKEN']), os.environ['NC_HOSTPATH'])
        jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFzaGdhcmRAZmFtd2V0ZXJpbmdzLm5sIiwiZmlyc3RuYW1lIjpudWxsLCJsYXN0bmFtZSI6bnVsbCwiaWQiOiJ1c192NmpqNjliNnhjOGRrbiIsInJvbGVzIjoidXNlcixzdXBlciIsInRva2VuX3ZlcnNpb24iOiIzYjAxYzRjMDE1ODFhOTI4MTU4MTYyOTdhYjY2ZmQ3MTlkNDQ0Y2RjZTU3NzYyNTU2MzE5ZWQ5NjgyNzhmMzE4Y2YzZmM2Nzk0YzUzMjE2YyIsImlhdCI6MTY2ODA2NjQ5MywiZXhwIjoxNjY4MTAyNDkzfQ.84hIwXGDjiGYjTT_T46mXDkgFLJmjrZovFhx09R0yGo"
        cls.client = NocoDBRequestsClient(JWTAuthToken(jwt_token), os.environ['NC_HOSTPATH'])
        cls.project = NocoDBProject("noco", "TEMP")
        cls.table_name = "TestCase"

    @classmethod
    def teardownClass(cls):
        print('done')

    def test_all(self):
        self.project_name = "TestProject8"
        self.table_name = "TestTable8"
        
#         self.step_project_create_requests()
#         self.step_table_create_requests()
        self.step_column_create_requests()
#         pjs = self.client.project_list()
#         for pj in pjs["list"]:
#             print(pj)
        
        #self.step_row_requests()
        #self.step_attachment() # COMMENTED BECAUSE IT WILL ADD NEW IMAGES EVERY RUN
        #self.step_project_delete_requests()
        
#     TODO check if this data base is actually added to root_db???
    def step_project_create_requests(self):
        print('test_project_create_requests')
 
        
        project_info = {
#             "prefix": "bla", # TODO: unable to set prefix using this endpoint: https://all-apis.nocodb.com/#tag/Project/operation/project-create
            "title": self.project_name,
            "description": "Dit is gewoon een test!",
#             "is_meta": False,
#             "meta": "bla",
        }
        self.client.project_create(project_info)
        
        projects = self.client.project_list()
        #print(projects)
        
        project_names = [project['title'] for project in projects['list']]
        self.assertTrue(self.project_name in project_names)
        

    def step_table_create_requests(self):
        print('test_table_create_requests')
        project_id = self.get_project_id(self.project_name)
        tables = self.client.table_list(project_id)
        
        print('tables')
        for table in tables['list']:
            print(table)
        print('tables')

        table_names = [table['title'] for table in tables['list']]
        self.assertFalse(self.table_name in table_names)
          
        # TODO hier verder table create en project create doesnt work, misschien is de token niet goed???
        table_info = {
            'table_name': self.table_name,
            'title': self.table_name,
            'show_as': self.table_name,
            'columns': [{
                'uidt': 'ID'
            }]
        }
        response = self.client.table_create(project_id, table_info)
#         print('test')
        print(response)
        
        tables = self.client.table_list(project_id)
        
        for table in tables['list']:
            print(table)
            
    def step_column_create_requests(self):
        print("Column create requests")
        project_id = self.get_project_id("TestProject")
        tables = self.client.table_list(project_id)
        print(project_id)
        print(tables)
        for table in tables['list']:
            print(table)
            
        
#         result = self.client.table_column_list("md_toukkmcz6kh4y0")
#         print(result)
        column_info = {
            "uidt": "SingleLineText",
#             "title": "Title testje",
#             "column_name": "Name testje",
#             "clen": 512
        }
        result = self.client.table_column_create("md_o63842awijfaq0", column_info)
        print(result)
#         self.table_column_set_primary(columnId)

    def step_row_requests(self):
        print('test_row_requests')
        #print("get initial results")
        initial_results = self.client.table_row_list(self.project, self.table_name)
        #print(f"initial_results={initial_results}")
        self.assertEqual(len(initial_results['list']), 1)
        self.assertEqual(initial_results['list'][0]['Title'], 'test-case-1')
          
        row_id = initial_results['list'][0]['Id']
        row_info = {
            "Title": "test-case-2"
        }
        self.client.table_row_update(self.project, self.table_name, row_id, row_info)
          
        #print("find reinserted record by title")
        found_records = self.client.table_row_list(self.project, self.table_name, EqFilter("Title", "test-case-2"))
        self.assertEqual(len(found_records['list']), 1)
        self.assertEqual(found_records['list'][0]['Title'], 'test-case-2')
          
        #print("delete first record")
        row_id = initial_results['list'][0]['Id']
        self.client.table_row_delete(self.project, self.table_name, row_id)
          
        #print("reinsert initial result")
        row_info = {
            "Title": initial_results['list'][0]['Title']
        }
        created_record = self.client.table_row_create(self.project, self.table_name, row_info)
          
        #print("get reinserted record")
        row_id = created_record['Id']
        found_record = self.client.table_row_detail(self.project, self.table_name, row_id)
        self.assertEqual(found_record['Title'], 'test-case-1')
          
        #print("find reinserted record by title")
        found_records = self.client.table_row_list(self.project, self.table_name, InFilter("Title", "test-case-1"))
        self.assertEqual(len(found_records['list']), 1)
        self.assertEqual(found_records['list'][0]['Title'], 'test-case-1')

    def step_attachment(self):
        buffer = self.convert_image_to_buffer(r"test_image.jpg")
        upload_result = self.client.storage_upload(r"test_image.jpg", buffer, params={'path': "noco/UnitTest/TestCase/Attachments"})
        self.assertEqual(len(upload_result), 1)
        self.assertTrue("url" in upload_result[0])
        self.assertTrue("title" in upload_result[0])
        self.assertTrue("mimetype" in upload_result[0])
        self.assertTrue("size" in upload_result[0])
         
        records = self.client.table_row_list(self.project, self.table_name, InFilter("Title", "test-case"))
        record = records['list'][0]
        row_id = record['Id']
        row_info = {
            "Attachment": json.dumps(upload_result)
        }
        self.client.table_row_update(self.project, self.table_name, row_id, row_info)

    def step_project_delete_requests(self):
        print('test_project_delete_requests')
        project_id = self.get_project_id(self.project_name)
         
        self.client.project_delete(project_id)
         
        projects = self.client.project_list()
        project_names = [project['title'] for project in projects['list']]
        
        self.assertFalse(self.project_name in project_names)
        
        
        
        
        
        
        
        
    # HELPERS    
    def get_project_id(self, title):
        projects = self.client.project_list()
        for project in projects['list']:
            if project['title'] == title:
                return project['id']
        return None
    
    def convert_image_to_buffer(self, filename):
        from io import BytesIO
        image = Image.open(filename).convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer
        
if __name__ == '__main__':
    print("Run as -> Python unit-test")
    