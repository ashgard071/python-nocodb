import os
from nocodb.nocodb import NocoDBProject, APIToken, JWTAuthToken
from nocodb.filters import InFilter, EqFilter
from nocodb.infra.requests_client import NocoDBRequestsClient


NC_PROJECT_NAME = "SmartGallery"
NC_PROJECT = NocoDBProject("noco", NC_PROJECT_NAME)
NC_FIELD_FILENAME_MAX_LENGTH = 512
NC_TABLE_FILES_NAME = "Files"


if __name__=="__main__":
    client = NocoDBRequestsClient(APIToken(os.environ['NC_TOKEN']), os.environ['NC_HOSTPATH'])
    #records = client.table_row_list(NC_PROJECT, NC_TABLE_FILES_NAME)
    #print(records)
    
    result = client.storage_upload(r"C:\Users\ashgard.weterings\Downloads\psu.jpg", params={'path': "noco/SmartGallery/Files/Thumbnail"})
    print(result)
    
    
    #res = [
    #    {
    #        "url":"http://localhost:8080/download/noco/SmartGallery/Files/Thumbnail/QIyUe1.jpg",
    #        "title": "psu.jpg",
    #        "mimetype": "image/jpeg",
    #        "size": 47409
    #    }
    #]
    #
    #try:
    #    json.loads(res)
    #    print('Yes')
    #except Exception as e:
    #    print('No')
    #
    #
    ##expected = "[{\"url\":\"http://localhost:8080/download/noco/SmartGallery/Files/Thumbnail/YMqDpD.jpg\",\"title\":\"psu.jpg\",\"mimetype\":\"image/jpeg\",\"size\":47409}]"
    ##
    ##print(res)
    #import json
    ##print(json.dumps(res))
    ##print(expected)
    #
    #row_info = {
    #    "Filename": "testje5",
    #    "Size (Mb)": 1.5,
    #    "Thumbnail": json.dumps(res)
    #}
    ##result = client.table_row_create(NC_PROJECT, NC_TABLE_FILES_NAME, row_info)