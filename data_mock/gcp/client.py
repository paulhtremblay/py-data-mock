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

def _check_meta(m:Union[Dict, None]):
    if m == None:
        return
    if not  isinstance(m, dict):
        raise DataValidationError('meta must be dict')

def check_data_func(data:list, m:dict):
    _check_data(data)
    _check_meta(m)

class UserDecorators():
    def check_data(func)-> Callable:
        def inner(self, data:list, m:dict):
            check_data_func(data, m)
            return func(self, data, m)
        return inner


class Client:

    def __init__(self, project:Union[str, None] = None, 
            mock_list_of_tables = None):
        self.project = project
        self.__list_of_tables = mock_list_of_tables

    def query(self, 
            query:str,
            *args, 
            **kwargs
              ) -> RowIterator:
        return self.run_query(data = None, m = {})

    @UserDecorators.check_data
    def run_query(self, 
            data:Union[List[List[tuple]], None] = None, 
            m:Union[dict, None] = None):
        if data == None:
            data = []
        if m == None:
            m = {}
        return RowIterator(data = data, m = m)

    def create_table(self):
        raise NotImplementedError()

    def delete_table(self):
        raise NotImplementedError()

    def list_tables(self):
        raise NotImplementedError()

    def load_table_from_uri(self):
        raise NotImplementedError()

    def get_table(self):
        raise NotImplementedError()

