from typing import Optional
from ..nocodb import (
    NocoDBClient,
    NocoDBProject,
    AuthToken,
    WhereFilter,
)
from ..api import NocoDBAPI
from ..utils import get_query_params

import requests
from requests_toolbelt import MultipartEncoder
from mimetypes import MimeTypes
from nocodb.filters import EqFilter

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


    def project_create(
        self,
        body
    ):
        return self.__session.post(
            self.__api_info.get_project_uri(), 
            json=body
        ).json()
        
    def project_update(
        self,
        projectId,
        body
    ):
        return self.__session.patch(
            self.__api_info.get_project_detail_uri(projectId), 
            json=body
        ).json()
        
    def project_delete(
        self,
        projectId
    ):
        return self.__session.delete(
            self.__api_info.get_project_detail_uri(projectId)
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

    def table_read(
        self,
        tableId: str
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_detail_uri(tableId)
        ).json()
    
    # DB column : https://all-apis.nocodb.com/#tag/DB-table-column
    
    def table_column_create(
        self,
        tableId: str,
        body: dict
    ):
        return self.__session.post(
            self.__api_info.get_table_column_uri(tableId), 
            json=body
        ).json()

    def table_column_set_primary(
        self,
        columnId: str
    ):
        return self.__session.post(
            self.__api_info.get_table_column_primary_uri(columnId)
        ).json()
        
    def table_column_delete(
        self,
        columnId: str
    ):
        return self.__session.delete(
            self.__api_info.get_table_column_detail_uri(columnId)
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
    
    def table_row_find_one(
        self,
        project: NocoDBProject,
        table: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None,
    ) -> dict:
        response = self.__session.get(
            self.__api_info.get_table_row_find_uri(project, table),
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

    def table_row_ltar_update(
        self, project: NocoDBProject, table: str, row_id: int, fields: dict
    ) -> dict:
        try:
            responses = []
            for column_name in fields:
                ltar_specs = fields[column_name]
                if isinstance(ltar_specs, dict):
                    lr_records = self.table_row_list(project, ltar_specs['lt_table'], EqFilter(ltar_specs['lt_column'], ltar_specs['lt_value']))
                    lr_recordId = lr_records['list'][0]['Id']
                    response = self.__session.post(
                        self.__api_info.get_row_ltar_uri(project, table, row_id, column_name, lr_recordId),
                    ).json()
                    responses.append(response)
            return responses
        except Exception as e:
            return {'msg': e}

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

    # DB view: https://all-apis.nocodb.com/#tag/DB-view
    
    def table_view_list(
        self,
        tableId: str
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_view_uri(tableId)
        ).json()

    def table_view_update(
        self,
        viewId: str,
        body: dict
    ) -> dict:
        return self.__session.patch(
            self.__api_info.get_table_view_detail_uri(viewId),
            json=body
        ).json()

    def table_grid_view_create(
        self,
        tableId: str,
        body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_grid_view_uri(tableId),
            json=body
        ).json()
        
    def table_gallery_view_create(
        self,
        tableId: str,
        body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_gallery_view_uri(tableId),
            json=body
        ).json()

    def table_view_hide_all_columns(
        self,
        viewId: str,
        filter_obj: Optional[WhereFilter] = None,
        params: Optional[dict] = None    
    ) -> dict:
        print(get_query_params(filter_obj, params))
        return self.__session.post(
            self.__api_info.get_table_view_hide_all_columns_uri(viewId),
            params=get_query_params(filter_obj, params),
        ).json()
        
    def table_view_column_list(
        self,
        viewId: str
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_view_column_uri(viewId)
        ).json()

    def table_view_column_update(
        self,
        viewId: str,
        columnId: str,
        body: dict
    ) -> dict:
        return self.__session.patch(
            self.__api_info.get_table_view_column_detail_uri(viewId, columnId),
            json=body
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
            self.__api_info.get_table_view_row_uri(project, table, view),
            params=get_query_params(filter_obj, params),
        )
        return response.json()

    # DB filter: https://all-apis.nocodb.com/#tag/DB-table-filter
    
    def table_filter_list(
        self,
        viewId: str
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_filter_uri(viewId)
        ).json()
        
    def table_filter_create(
        self,
        viewId: str,
        body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_filter_uri(viewId),
            json=body
        ).json()
        
    # DB sort: https://all-apis.nocodb.com/#tag/DB-table-sort
    
    def table_sort_list(
        self,
        viewId: str
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_sort_uri(viewId)
        ).json()
        
    def table_sort_create(
        self,
        viewId: str,
        body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_sort_uri(viewId),
            json=body
        ).json()

    # DB table Webhook: https://all-apis.nocodb.com/#tag/DB-table-webhook

    def table_webhook_list(
        self,
        tableId: str
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_webhook_uri(tableId)
        ).json()
        
    def table_webhook_filter_list(
        self,
        hookId: str,
    ) -> dict:
        return self.__session.get(
            self.__api_info.get_table_webhook_filter_uri(hookId)
        ).json()
        
    def table_webhook_create(
        self,
        tableId: str,
        body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_webhook_uri(tableId),
            json=body
        ).json()
        
    def table_webhook_filter_create(
        self,
        hookId: str,
        body: dict
    ) -> dict:
        return self.__session.post(
            self.__api_info.get_table_webhook_filter_uri(hookId),
            json=body
        ).json()

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

    
