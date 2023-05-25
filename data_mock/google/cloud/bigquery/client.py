from .  import table as _table
from .job import query as job_query
from . import retry as retries
from . import dataset as _dataset
import data_mock.mock_helpers.provider as provider
import data_mock.google.cloud.bigquery.job as job
from data_mock.google.cloud.bigquery.job  import LoadJobConfig
from data_mock.google.cloud.bigquery.table  import Table
from data_mock.google.cloud.bigquery.table  import TableReference
from data_mock.google.cloud.bigquery.table  import TableListItem
from data_mock.exceptions import InvalidMockData
import data_mock.exceptions as exceptions

from typing import Union, Optional, Sequence

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
        self.data_provider = provider.ProvideData()
        if mock_data:
            self.data_provider.add_data(data = mock_data, tag = 'default')
        self.register_initial_mock_data()

    def register_mock_data(self, key, mock_data):
        self.data_provider.add_data(data = mock_data, tag = key)

    def register_initial_mock_data(self):
        pass

    def query(self, query,
        job_config: Optional[job_query.QueryJobConfig] = None,
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
            data, m = self.data_provider.get_data(key)
            if not data:
                raise exceptions.InvalidMockData(f'{key} not found in registered_data')
        else:
            try:
                data, m = self.data_provider.get_data('default')
            except TypeError:
                raise exceptions.InvalidMockData(f'bad class')
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

    def load_table_from_uri(
        self,
        source_uris: Union[str, Sequence[str]],
        destination: Union[_table.Table, _table.TableReference, _table.TableListItem, str],
        job_id: str = None,
        job_id_prefix: str = None,
        location: str = None,
        project: str = None,
        job_config: LoadJobConfig = None,
        retry: retries.Retry = DEFAULT_RETRY,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
        ) -> job.LoadJob:
        load_job = job.LoadJob(job_ref = None, source_uris = source_uris, destination = destination, 
            new_job_config = None)
        load_job._begin(retry=retry, timeout=timeout)
        if not isinstance(job_config, LoadJobConfig):
            raise InvalidMockData('job_config must be of type LoadJobConfig')
        return load_job

    def get_table(
        self,
        table: Union[Table, TableReference, TableListItem, str],
        retry: retries.Retry = DEFAULT_RETRY,
        timeout: TimeoutType = DEFAULT_TIMEOUT,
    ) -> Table:
        if isinstance(table,str):
            table_ref = self._mock_make_table_ref(table_id = table)
        else:
            table_ref = table
        return Table(table_ref = table_ref)

    def _mock_make_table_ref(self, table_id:str) -> str:
        fields = table_id.split()
        if len(fields) == 3:
            return table_id
        else:
            if not self.project:
                project = 'not_passesd'
            else:
                project = self.project
            if len(fields) == 2:
                return f'{project}.{table_id}'
            elif len(fields) == 1:
                return f'{project}.dataset_not_passed.{table_id}'
            else:
                raise ValueError('bad sring')


    def _get_sql_key(self, query:str)-> str:
        for line in query.split('\n'):
            if 'py-bigquery-mock-register:' in line:
                fields = line.split(':')
                if len(fields) != 2:
                    raise exceptions.InvalidMockData('hint should be in format "py-bigquery-mock-register: key"')
                return fields[1].strip()

