from typing import List, Dict, Union, Any


class ServerResponse:
    def __init__(self, id: str, success: bool, error: str = None):
        self.id = id
        self.success = success
        self.error = error


class ConnectionResult(ServerResponse):
    def __init__(self, id: str, success: bool, job: str, error: str = None):
        super().__init__(id, success, error)
        self.job = job


class ColumnMetaData:
    def __init__(self, display_size: int, label: str, name: str, type: str):
        self.display_size = display_size
        self.label = label
        self.name = name
        self.type = type


class QueryMetaData:
    def __init__(self, column_count: int, columns: List[ColumnMetaData], job: str):
        self.column_count = column_count
        self.columns = columns
        self.job = job


class QueryResult(ServerResponse):
    def __init__(
        self,
        id: str,
        success: bool,
        metadata: QueryMetaData,
        is_done: bool,
        data: Any,
        error: str = None,
    ):
        super().__init__(id, success, error)
        self.metadata = metadata
        self.is_done = is_done
        self.data = data


class Rows(List[Dict[str, Union[str, int, bool]]]):
    pass


class JDBCOptions:
    def __init__(
        self,
        naming: str = None,
        libraries: List[str] = None,
        full_open: bool = None,
        transaction_isolation: str = None,
    ):
        self.naming = naming
        self.libraries = libraries
        self.full_open = full_open
        self.transaction_isolation = (
            transaction_isolation
            if transaction_isolation
            in ["read uncommitted", "read committed", "repeatable read", "serializable"]
            else "none"
        )
