from data_mock.psycopg2.cursor import Cursor
import data_mock.mock_helpers.provider as provider

class Connect:

    def __init__(self, dsn=None, connection_factory=None, 
            mock_data = None,  **kwargs):
        self.data_provider = provider.ProvideData()
        if mock_data:
            self.data_provider.add_data(data = mock_data, tag = 'default')
        self.register_initial_mock_data()
        
    def register_initial_mock_data(self):
        pass

    def register_mock_data(self, key, mock_data):
        self.data_provider.add_data(data = mock_data, tag = key)

    def cursor(self, cursor_factory = Cursor,  *args, **kwargs):
        return cursor_factory(data_provider = self.data_provider)
