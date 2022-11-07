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

    def get_table_column_uri(self, tableId: int) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "tables",
                str(tableId),
                "columns"
            )
        )

    def get_table_column_detail_uri(self, tableId: int, columnId: int) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "tables",
                str(tableId),
                "columns",
                str(columnId)
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

    def get_table_view_uri(self, project: NocoDBProject, table: str, view: str) -> str:
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

    def get_project_uri(
        self,
    ) -> str:
        return "/".join(
            (
                self.__base_meta_uri,
                "projects"
            )
        )
        
    def get_project_id_uri(
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
        
    def get_storage_uri(
        self,
    ) -> str:
        return "/".join(
            (
                self.__base_storage_uri,
                "upload"
            )
        )
        