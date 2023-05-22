from . import exceptions
from .  import table as _table
from .job import query as job_query
from . import retry as retries
from . import dataset as _dataset
import data_mock.mock_helpers.provider as provider

from typing import Union, Optional

# these values do nothing
DEFAULT_RETRY = None
DEFAULT_TIMEOUT = None
DEFAULT_JOB_RETRY = None
TimeoutType = Union[float, None]

class Client:

    def __init__(self, project = None, mock_data = None, 
            mock_list_of_tables = None):
        self.project = project
        self.__list_of_tables = mock_list_of_tables
        self._data_provider = provider.ProvideData()
        if mock_data:
            self._data_provider.add_data(data = mock_data, tag = 'default_')

    def register_mock_data(self, key, mock_data):
        self._data_provider.add_data(data = mock_data, tag = key)

    def query(self, query,
        job_config: job_query.QueryJobConfig = None,
        job_id: str = None,
        job_id_prefix: str = None,
        location: str = None,
        project: str = None,
        retry: retries.Retry = DEFAULT_RETRY,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
        job_retry: retries.Retry = DEFAULT_JOB_RETRY,
              ):
        """
        all args ignored except query
        """
        key = self._get_sql_key(query)
        if key:
            data, m = self._data_provider.get_data(key)
            if not data:
                raise exceptions.InvalidMockData(f'{key} not found in registered_data')
        else:
            data, m = self._data_provider.get_data('default_')
        return _table.RowIterator(data = data, m = m)

    def create_table(self,
            table: Union[str, _table.Table, _table.TableReference, _table.TableListItem],
            exists_ok: bool = False,
            retry: retries.Retry = DEFAULT_RETRY,
            timeout: TimeoutType = DEFAULT_TIMEOUT,
        ):
        """
        all args ignored
        """

        if  hasattr(table, 'dataset_id')\
                and hasattr(table, 'project')\
                and  hasattr(table, 'schema'):
                    pass
        else:
            table_obj = _table.Table(table)
            table = table_obj

        if self.__list_of_tables == None:
            self.__list_of_tables = []
        self.__list_of_tables.append(table) 
        return table

    def delete_table(self,
            table: Union[_table.Table, _table.TableReference, _table.TableListItem, str],
            retry: retries.Retry = DEFAULT_RETRY,
            timeout: TimeoutType = DEFAULT_TIMEOUT,
            not_found_ok: bool = False,
        ):
        """
        all args ignored
        """
        if self.__list_of_tables == None and not_found_ok == False:
            raise exceptions.TableNotFound('table not found')
        elif self.__list_of_tables == None and not_found_ok == True:
            pass
        else:
            if hasattr(table, 'table_id'):
                _id = table.table_id
            else:
                _id = table
            for i in self.__list_of_tables:
                if i.table_id == _id:
                    self.__list_of_tables.remove(i)

    def list_tables(self,
         dataset: Union[_dataset.Dataset, _dataset.DatasetReference, _dataset.DatasetListItem, str],
         max_results: Optional[int] = None,
         page_token: str = None,
         retry: retries.Retry = DEFAULT_RETRY,
         timeout: TimeoutType = DEFAULT_TIMEOUT,
                    page_size: Optional[int] = None):
        if self.__list_of_tables == None:
            return []
        return self.__list_of_tables


    def _get_sql_key(self, query):
        for line in query.split('\n'):
            if 'py-bigquery-mock-register:' in line:
                fields = line.split(':')
                if len(fields) != 2:
                    raise exceptions.InvalidMockData('hint should be in format "py-bigquery-mock-register: key"')
                return fields[1].strip()

