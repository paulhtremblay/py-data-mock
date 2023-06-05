from collections import OrderedDict

import data_mock.mock_helpers.provider as provider
from data_mock.psycopg2.exceptions import ProgrammingError
import data_mock.exceptions as exceptions

class Cursor:

    def __init__(self, cursor_factory = None, mock_data = None, use_dict = False, 
                data_provider = None,  *args, **kwargs):
        if data_provider != None:
            self.data_provider = data_provider
        else:
            self.data_provider = provider.ProvideData()
        if mock_data:
            self.data_provider.add_data(data = mock_data, tag = 'default')
        self.register_initial_mock_data()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def execute(self, query:str):
        """
        all args ignored except query
        """

        key = self._get_sql_key(query)
        if key:
            self.data, self.meta_data = self.data_provider.get_data(key)
            if not self.data:
                raise exceptions.InvalidMockData(f'{key} not found in registered_data')
        else:
            try:
                self.data, self.meta_data = self.data_provider.get_data('default')
            except TypeError:
                raise exceptions.InvalidMockData(f'bad class')

    def register_initial_mock_data(self):
        pass

    def register_mock_data(self, key, mock_data):
        self.data_provider.add_data(data = mock_data, tag = key)


    def construct_row(self, row:list) -> tuple:
        new_row = []
        for data_obj in row:
            new_row.append(data_obj.value)
        return tuple(new_row)


    def fetchmany(self, n:int)-> list:
        counter = 0
        final = []
        if not hasattr(self, 'data'):
            raise ProgrammingError('no result to fetch')
        if not self.data:
            return
        for counter, row in enumerate(self.data):
            new_row = self.construct_row(row)
            final.append(new_row)
            if counter + 1 == n:
                return final
        return final

    def _get_sql_key(self, query:str)-> str:
        for line in query.split('\n'):
            if 'py-postgres-mock-register:' in line:
                fields = line.split(':')
                if len(fields) != 2:
                    raise exceptions.InvalidMockData('hint should be in format "py-postgres-mock-register: key"')
                return fields[1].strip()
