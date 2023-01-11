from enum import Enum
from .nocodb import NocoDBProject


class NocoDBAPIUris(Enum):
    V1_DB_DATA_PREFIX = "api/v1/db/data"
    V1_DB_META_PREFIX = "api/v1/db/meta"
    V1_DB_STORAGE_PREFIX = "api/v1/db/storage"


class NocoDBAPI:
    def __init__(self, base_uri: str):
        self.__base_data_uri = (
            f"{base_uri}/{NocoDBAPIUris.V1_DB_DATA_PREFIX.value}"
        )
        self.__base_meta_uri = (
            f"{base_uri}/{NocoDBAPIUris.V1_DB_META_PREFIX.value}"
        )
        self.__base_storage_uri = (
            f"{base_uri}/{NocoDBAPIUris.V1_DB_STORAGE_PREFIX.value}"
        )
        
    def get_project_uri(
        self,
    ) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "projects"
            )
        )
        
    def get_project_detail_uri(
        self,
        project_id: str
    ) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "projects",
                project_id
            )
        )
        
    def get_table_uri(
        self,
        projectId: str,
    ) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "projects",
                projectId,
                "tables"
            )
        )
        
    def get_table_detail_uri(
        self,
        tableId: str,
    ) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "tables",
                tableId
            )
        )
        
        
    def get_table_view_uri(self, tableId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'tables',
                tableId,
                'views'
            )
        )
        
    def get_table_view_detail_uri(self, viewId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'views',
                viewId
            )
        )
        
    def get_table_grid_view_uri(self, tableId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'tables',
                tableId,
                'grids'
            )
        )
        
    def get_table_gallery_view_uri(self, tableId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'tables',
                tableId,
                'galleries'
            )
        )
        
    def get_table_view_hide_all_columns_uri(self, viewId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'views',
                viewId,
                'hide-all'
            )
        )
        
    def get_table_view_column_uri(self, viewId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'views',
                viewId,
                'columns'
            )
        )
        
    def get_table_view_column_detail_uri(self, viewId: str, columnId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'views',
                viewId,
                'columns',
                columnId
            )
        )
        
    def get_table_view_row_uri(self, project: NocoDBProject, table: str, view: str) -> str:
        return "/".join(
            (
                self.__base_data_uri,
                project.org_name,
                project.project_name,
                table,
                'views',
                view
            )
        )
        
    def get_table_filter_uri(self, viewId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'views',
                viewId,
                'filters'
            )
        )
        
    def get_table_sort_uri(self, viewId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                'views',
                viewId,
                'sorts'
            )
        )

    def get_table_column_uri(self, tableId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "tables",
                str(tableId),
                "columns"
            )
        )
        
    def get_table_column_detail_uri(self, columnId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "columns",
                str(columnId)
            )
        )
        
    def get_table_column_primary_uri(self, columnId: str) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "columns",
                str(columnId),
                "primary"
            )
        )
        
    def get_table_row_uri(self, project: NocoDBProject, table: str) -> str:
        return "/".join(
            (
                self.__base_data_uri,
                project.org_name,
                project.project_name,
                table,
            )
        )
        
    def get_table_row_find_uri(self, project: NocoDBProject, table: str) -> str:
        return "/".join(
            (
                self.__base_data_uri,
                project.org_name,
                project.project_name,
                table,
                "find-one"
            )
        )
        
    def get_row_detail_uri(
        self, project: NocoDBProject, table: str, row_id: int
    ):
        return "/".join(
            (
                self.__base_data_uri,
                project.org_name,
                project.project_name,
                table,
                str(row_id),
            )
        )
    
    def get_row_ltar_uri(
        self, project: NocoDBProject, table: str, row_id: int, column_name: str, lt_row_id: int
    ):
        return "/".join(
            (
                self.__base_data_uri,
                project.org_name,
                project.project_name,
                table,
                str(row_id),
                'mm',
                column_name,
                str(lt_row_id)
            )
        )    

    def get_nested_relations_rows_list_uri(
        self,
        project: NocoDBProject,
        table: str,
        relation_type: str,
        row_id: int,
        column_name: str,
    ) -> str:
        return "/".join(
            (
                self.__base_data_uri,
                project.org_name,
                project.project_name,
                table,
                str(row_id),
                relation_type,
                column_name,
            )
        )
        
    def get_table_webhook_uri(
        self,
        tableId: str
    ) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "tables",
                tableId,
                "hooks"
            )
        )
        
    def get_table_webhook_filter_uri(
        self,
        hookId: str
    ) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "hooks",
                hookId,
                "filters"
            )
        )
        
    def get_storage_uri(
        self,
    ) -> str:
        return "/".join(
            (
                self.__base_storage_uri,
                "upload"
            )
        )
        