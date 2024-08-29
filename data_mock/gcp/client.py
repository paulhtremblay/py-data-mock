from collections.abc import Callable
from data_mock.gcp.table  import RowIterator
from data_mock.gcp import table 
from data_mock.gcp.table  import Table
from data_mock.gcp.table  import TableReference
from data_mock.gcp.table  import TableListItem
from data_mock.gcp.job  import LoadJobConfig
import data_mock.gcp.job as job

from typing import Union, Optional, Sequence, Type, TypeVar, Optional, List, Dict

class DataValidationError(Exception):
    pass

def _check_data(data:Union[List, None]) -> bool:
    if data == None:
        return True
    elif not isinstance(data, list):
        raise DataValidationError('data must be a list')
    for i in data:
        if not isinstance(i, list):
            raise DataValidationError('data must be a list')
        if not isinstance(i[0], tuple):
            raise DataValidationError('data must be a list list tuple')
        if len(i[0]) != 2:
            raise DataValidationError('tuple must be (name, value)')
    return True

def _check_meta(meta:Union[Dict, None]):
    if meta == None:
        return
    if not  isinstance(meta, dict):
        raise DataValidationError('meta must be dict')

def check_data_func(data:list, meta:dict):
    _check_data(data)
    _check_meta(meta)

def check_mock_list_of_tables(
        mock_list_of_tables:Union[List[Table], None] = None):
    if mock_list_of_tables == None:
        return
    for i in mock_list_of_tables:
        if not isinstance(i, Table):
            raise  DataValidationError(
                    'items passed to mock_list_of tables must be Table objects')

class UserDecorators():
    def check_data(func)-> Callable:
        def inner(self, data:Union[list, None] = None, 
                meta:Union[dict, None] = None):
            check_data_func(data, meta)
            return func(self, data, meta)
        return inner

class Client:

    def __init__(self, project:Union[str, None] = None, 
            ):
        self.project = project
        self.initialize_table_list()
        check_mock_list_of_tables(self.list_of_tables)

    def create_table_list(self, tables:List[Dict] = None):
        self.list_of_tables = []
        if tables == None:
            return
        if not isinstance(tables, list):
            raise  DataValidationError('table must be a list of dicts')
        for i in tables:
            if not isinstance(i, dict):
                raise  DataValidationError('Each item in initialize table must be a dict')
            self.list_of_tables.append(
                    Table(**i)
                    )

    def initialize_table_list(self, tables:List[Dict] = None) :
        self.list_of_tables = []

    @UserDecorators.check_data
    def run_query(self, 
            data:Union[List[List[tuple]], None] = None, 
            meta:Union[dict, None] = None) -> RowIterator:
        if data == None:
            data = []
        if meta == None:
            meta = {}
        return RowIterator(data = data, meta = meta)
    #===========================================================================#

    def create_table(self, table:Union[Table, str], 
            *args, **kwargs) -> Table:
        if isinstance(table, Table):
            pass
        else:
            #assume the table id is passed
            table = Table(table_ref = table)
        self.list_of_tables.append(table)
        return table

    def dataset(self, table_id:str, *args, **kwargs) -> object:
        class Mock:
            def table(self, args, **kwargs)-> None:
                return 
        return Mock()

    def cancel_job(self, *args, **kwargs):
        raise NotImplementedError()

    def close(self, *args, **kwargs):
         raise NotImplementedError()

    def copy_table(self, *args, **kwargs):
        raise NotImplementedError()

    def create_dataset(self, *args, **kwargs):
        raise NotImplementedError()

    def create_job(self, *args, **kwargs):
        raise NotImplementedError()

    def create_routine(self, *args, **kwargs):
        raise NotImplementedError()

    def default_load_job_config(self, *args, **kwargs):
        raise NotImplementedError()

    def default_query_job_config(self, *args, **kwargs):
        raise NotImplementedError()

    def delete_dataset(self, *args, **kwargs):
        raise NotImplementedError()

    def delete_job_metadata(self, *args, **kwargs):
        raise NotImplementedError()

    def delete_model(self, *args, **kwargs):
        raise NotImplementedError()

    def delete_routine(self, *args, **kwargs):
         raise NotImplementedError()

    def delete_table(self, *args, **kwargs):
        raise NotImplementedError()

    def extract_table(self, *args, **kwargs):
        raise NotImplementedError()

    def from_service_account_info(self, *args, **kwargs):
        raise NotImplementedError()

    def from_service_account_json(self, *args, **kwargs):
         raise NotImplementedError()

    def get_dataset(self, *args, **kwargs):
        raise NotImplementedError()

    def get_iam_policy(self, *args, **kwargs):
        raise NotImplementedError()

    def get_job(self, *args, **kwargs):
         raise NotImplementedError()

    def get_model(self, *args, **kwargs):
        raise NotImplementedError()

    def get_routine(self, *args, **kwargs):
        raise NotImplementedError()

    def get_service_account_email(self, *args, **kwargs):
         raise NotImplementedError()

    def get_table(self, *args, **kwargs):
        raise NotImplementedError()

    def insert_rows(self, *args, **kwargs):
        raise NotImplementedError()

    def insert_rows_from_dataframe(self, *args, **kwargs):
         raise NotImplementedError()

    def insert_rows_json(self, *args, **kwargs):
        raise NotImplementedError()

    def job_from_resource(self, *args, **kwargs):
        raise NotImplementedError()

    def list_datasets(self, *args, **kwargs):
         raise NotImplementedError()

    def list_jobs(self, *args, **kwargs):
        raise NotImplementedError()

    def list_models(self, *args, **kwargs):
        raise NotImplementedError()

    def list_partitions(self, *args, **kwargs):
        raise NotImplementedError()

    def list_projects(self, *args, **kwargs):
        raise NotImplementedError()

    def list_routines(self, *args, **kwargs):
        raise NotImplementedError()

    def list_rows(self, *args, **kwargs):
        raise NotImplementedError()

    def list_tables(self):
        return self.list_of_tables

    def load_table_from_dataframe(self, *args, **kwargs):
        raise NotImplementedError()

    def load_table_from_file(self, *args, **kwargs):
        raise NotImplementedError()

    def load_table_from_json(self, *args, **kwargs):
        raise NotImplementedError()

    def load_table_from_uri(self, *args, **kwargs):
        raise NotImplementedError()

    def location(self, *args, **kwargs):
        raise NotImplementedError()

    def project(self, *args, **kwargs):
        raise NotImplementedError()

    def query(self, 
            query:str,
            *args, 
            **kwargs
              ) -> RowIterator:
        return self.run_query(data = None, meta = {})

    def query_and_wait(self, *args, **kwargs):
        raise NotImplementedError()

    def schema_from_json(self, *args, **kwargs):
        raise NotImplementedError()

    def schema_to_json(self, *args, **kwargs):
        raise NotImplementedError()

    def set_iam_policy(self, *args, **kwargs):
        raise NotImplementedError()

    def test_iam_permissions(self, *args, **kwargs):
        raise NotImplementedError()

    def update_dataset(self, *args, **kwargs):
        raise NotImplementedError()

    def update_model(self, *args, **kwargs):
        raise NotImplementedError()

    def update_routine(self, *args, **kwargs):
        raise NotImplementedError()

    def update_table(self, *args, **kwargs):
        raise NotImplementedError()
