from data_mock.psycopg2.cursor import Cursor
from data_mock.psycopg2.extras import RealDictCursor

import data_mock.mock_helpers.provider as provider

from typing import Union

class Connect:

    def __init__(self, dsn=None, connection_factory=None, 
            mock_data = None,  **kwargs):
        self.data_provider = provider.ProvideData()
        if mock_data:
            self.data_provider.add_data(data = mock_data, tag = 'default')
        self.register_initial_mock_data()
        
    def register_initial_mock_data(self):
        pass

    def register_mock_data(self, key:str, mock_data:list):
        self.data_provider.add_data(data = mock_data, tag = key)

    def cursor(self, cursor_factory: Union[Cursor, RealDictCursor] = Cursor) -> Union[Cursor, RealDictCursor]:
        return cursor_factory(data_provider = self.data_provider)
