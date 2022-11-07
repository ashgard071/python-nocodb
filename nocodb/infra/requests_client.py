from typing import Optional
from ..nocodb import (
    NocoDBClient,
    NocoDBProject,
    AuthToken,
    WhereFilter,
)
from ..api import NocoDBAPI
from ..utils import get_query_params

import os
import requests
import json
from requests_toolbelt import MultipartEncoder
from mimetypes import MimeTypes
from hachoir.parser.archive.sevenzip import Body

class NocoDBRequestsClient(NocoDBClient):
    def __init__(self, auth_token: AuthToken, base_uri: str):
        self.__session = requests.Session()
        self.__session.headers.update(
            auth_token.get_header(),
        )
        self.__session.headers.update({"Content-Type": "application/json"})
        self.__api_info = NocoDBAPI(base_uri)

    # Project: https://all-apis.nocodb.com/#tag/Project
    
    def project_list(
        self
    ):
        return self.__session.get(
            self.__api_info.get_project_uri()
        ).json()

#    TODO: unable to get this one working...
    def project_create(
        self,
        body
    ):
        return self.__session.post(
            self.__api_info.get_project_uri(), 
            json=body
        ).json()
        
    def project_delete(
        self,
        projectId
    ):
        return self.__session.delete(
            self.__api_info.get_project_id_uri(projectId)
        ).json()

    # DB table: 
    def table_list(
        self,
        projectId: str
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_uri(projectId)
        ).json()
    
    def table_create(
        self,
        projectId: str,
        body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_uri(projectId), 
            json=body
        ).json()

    # DB column : ...
    def table_column_list(
        self,
        tableId: int
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_column_uri(tableId)
        ).json()
    
    def table_column_create(
        self,
        tableId: int,
        columnId: int,
        body: dict
    ):
        return self.__session.post(
            self.__api_info.get_table_column_detail_uri(tableId, columnId), 
            json=body
        ).json()

    # DB table row: https://all-apis.nocodb.com/#tag/DB-table-row

    def table_row_list(
        self,
        project: NocoDBProject,
        table: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None,
    ) -> dict:

        response = self.__session.get(
            self.__api_info.get_table_row_uri(project, table),
            params=get_query_params(filter_obj, params),
        )
        return response.json()
    
    def table_row_create(
        self, project: NocoDBProject, table: str, body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_row_uri(project, table), json=body
        ).json()

    def table_row_detail(
        self, project: NocoDBProject, table: str, row_id: int
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_row_detail_uri(project, table, row_id),
        ).json()

    def table_row_update(
        self, project: NocoDBProject, table: str, row_id: int, body: dict
    ) -> dict:
        return self.__session.patch(
            self.__api_info.get_row_detail_uri(project, table, row_id),
            json=body,
        ).json()

    def table_row_delete(
        self, project: NocoDBProject, table: str, row_id: int
    ) -> int:
        return self.__session.delete(
            self.__api_info.get_row_detail_uri(project, table, row_id),
        ).json()

    def table_row_nested_relations_list(
        self,
        project: NocoDBProject,
        table: str,
        relation_type: str,
        row_id: int,
        column_name: str,
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_nested_relations_rows_list_uri(
                project, table, relation_type, row_id, column_name
            )
        ).json()

    # DB view row: https://all-apis.nocodb.com/#tag/DB-view-row
        
    def table_view_row_list(
        self,
        project: NocoDBProject,
        table: str,
        view: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None,
    ) -> dict:

        response = self.__session.get(
            self.__api_info.get_table_view_uri(project, table, view),
            params=get_query_params(filter_obj, params),
        )
        return response.json()

    # DB storage: https://all-apis.nocodb.com/#tag/Storage

    def storage_upload(
        self,
        filename,
        buffer,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None
    ):
        mimetype = MimeTypes().guess_type(filename)[0]
        form_data = MultipartEncoder(fields={'file': (filename, buffer, mimetype)})
        self.__session.headers.update({"Content-Type": form_data.content_type})
        r = self.__session.post(
            self.__api_info.get_storage_uri(), 
            params=get_query_params(filter_obj, params),
            data=form_data
        )
        self.__session.headers.update({"Content-Type": "application/json"})
        return r.json()

