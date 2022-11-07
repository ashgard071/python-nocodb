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
        # TODO test with JWT secret?
#        cls.client = NocoDBRequestsClient(APIToken(os.environ['NC_TOKEN']), os.environ['NC_HOSTPATH'])
        cls.client = NocoDBRequestsClient(JWTAuthToken('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFzaGdhcmRAZmFtd2V0ZXJpbmdzLm5sIiwiZmlyc3RuYW1lIjpudWxsLCJsYXN0bmFtZSI6bnVsbCwiaWQiOiJ1c192NmpqNjliNnhjOGRrbiIsInJvbGVzIjoidXNlcixzdXBlciIsInRva2VuX3ZlcnNpb24iOiIzYjAxYzRjMDE1ODFhOTI4MTU4MTYyOTdhYjY2ZmQ3MTlkNDQ0Y2RjZTU3NzYyNTU2MzE5ZWQ5NjgyNzhmMzE4Y2YzZmM2Nzk0YzUzMjE2YyIsImlhdCI6MTY2NzY1NzgzNiwiZXhwIjoxNjY3NjkzODM2fQ.RuocZfX7uCtX6xoiZNpixe6MRcAchuVeq8seYRsaAVE'), os.environ['NC_HOSTPATH'])
        cls.project = NocoDBProject("noco", "UnitTest")
        cls.table_name = "TestCase"

    @classmethod
    def teardownClass(cls):
        print('done')

#     TODO check if this data base is actually added to root_db???
    def test_project_create_requests(self):
        print('test_project_create_requests')
 
        project_info = {
            "title": "TestProject",
        }
        self.client.project_create(project_info)
         
        projects = self.client.project_list()
 
        project_names = [project['title'] for project in projects['list']]
        self.assertTrue('TestProject' in project_names)
        

    def test_table_create_requests(self):
        print('test_table_create_requests')
        project_id = self.get_project_id('TestProject')
        tables = self.client.table_list(project_id)

        table_names = [table['title'] for table in tables['list']]
        self.assertFalse('TestTable' in table_names)
          
        # TODO hier verder table create en project create doesnt work, misschien is de token niet goed???
        table_info = {
            'table_name': 'TestTable',
            'title': 'TestTable',
            'columns': [{
                'uidt': 'my-uidt'
            }]
        }
        response = self.client.table_create(project_id, table_info)
#         print('test')
        print(response)




#     def test_row_requests(self):
#         print('test_row_requests')
#         #print("get initial results")
#         initial_results = self.client.table_row_list(self.project, self.table_name)
#         #print(f"initial_results={initial_results}")
#         self.assertEqual(len(initial_results['list']), 1)
#         self.assertEqual(initial_results['list'][0]['Title'], 'test-case-1')
#          
#         row_id = initial_results['list'][0]['Id']
#         row_info = {
#             "Title": "test-case-2"
#         }
#         self.client.table_row_update(self.project, self.table_name, row_id, row_info)
#          
#         #print("find reinserted record by title")
#         found_records = self.client.table_row_list(self.project, self.table_name, EqFilter("Title", "test-case-2"))
#         self.assertEqual(len(found_records['list']), 1)
#         self.assertEqual(found_records['list'][0]['Title'], 'test-case-2')
#          
#         #print("delete first record")
#         row_id = initial_results['list'][0]['Id']
#         self.client.table_row_delete(self.project, self.table_name, row_id)
#          
#         #print("reinsert initial result")
#         row_info = {
#             "Title": initial_results['list'][0]['Title']
#         }
#         created_record = self.client.table_row_create(self.project, self.table_name, row_info)
#          
#         #print("get reinserted record")
#         row_id = created_record['Id']
#         found_record = self.client.table_row_detail(self.project, self.table_name, row_id)
#         self.assertEqual(found_record['Title'], 'test-case-1')
#          
#         #print("find reinserted record by title")
#         found_records = self.client.table_row_list(self.project, self.table_name, InFilter("Title", "test-case-1"))
#         self.assertEqual(len(found_records['list']), 1)
#         self.assertEqual(found_records['list'][0]['Title'], 'test-case-1')



#    COMMENTED BECAUSE IT WILL ADD NEW IMAGES EVERY RUN
#     def test_attachment(self):
#         buffer = self.convert_image_to_buffer(r"test_image.jpg")
#         upload_result = self.client.storage_upload(r"test_image.jpg", buffer, params={'path': "noco/UnitTest/TestCase/Attachments"})
#         self.assertEqual(len(upload_result), 1)
#         self.assertTrue("url" in upload_result[0])
#         self.assertTrue("title" in upload_result[0])
#         self.assertTrue("mimetype" in upload_result[0])
#         self.assertTrue("size" in upload_result[0])
#         
#         records = self.client.table_row_list(self.project, self.table_name, InFilter("Title", "test-case"))
#         record = records['list'][0]
#         row_id = record['Id']
#         row_info = {
#             "Attachment": json.dumps(upload_result)
#         }
#         self.client.table_row_update(self.project, self.table_name, row_id, row_info)
        

    
#     def test_project_delete_requests(self):
#         print('test_project_delete_requests')
#         project_id = self.get_project_id('TestProject')
#         
#         self.client.project_delete(project_id)
#         
#         projects = self.client.project_list()
#         project_names = [project['title'] for project in projects['list']]
#         
#         self.assertFalse('TestProject' in project_names)
        
        
        
        
        
        
        
        
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
    