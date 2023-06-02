from data_mock.exceptions import InvalidMockData
import data_mock.mock_helpers.provider as provider

class MockHelp:
    def __init__(self, mock_data, mock_max_rows, *args, **kwargs):
        self_provider = provider.ProvideData()
        self.mock_counter = -1
        self.mock_max_rows= mock_max_rows
        self.mock_data = mock_data
        if mock_data:
            self.data_provider.add_data(data = mock_data, tag = 'default')
        self.register_initial_mock_data()

    def register_mock_data(self, key, mock_data):
        self.data_provider.add_data(data = mock_data, tag = key)

    def register_initial_mock_data(self):
        pass


class MockCursor:

    def __init__(self, *args, **kwargs):
        self.data_provider = provider.ProvideData()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def execute(self, query, mock_data = None):
        """
        all args ignored except query
        """
        if mock_data:
            self.register_mock_data(mock_data = mock_data,key = 'default')
        self.data, self.meta_data = self.data_provider.get_data('default')

    def register_mock_data(self, key, mock_data):
        self.data_provider.add_data(data = mock_data, tag = key)

    def fetchmany(self, n):
        counter = 0
        final = []
        if not self.data:
            return
        new_row = []
        for counter, row in enumerate(self.data):
            for data_obj in row:
                new_row.append(data_obj.value)
            final.append(new_row)
            if counter + 1 == n:
                return final
        return final


    def cursor(self, *args, **kwargs):
        return self

    def _get_sql_key(self, query:str)-> str:
        for line in query.split('\n'):
            if 'py-bigquery-mock-register:' in line:
                fields = line.split(':')
                if len(fields) != 2:
                    raise exceptions.InvalidMockData('hint should be in format "py-bigquery-mock-register: key"')
                return fields[1].strip()

def connect(dsn=None, connection_factory=None, 
            cursor_factory=None,  **kwargs):
    return MockCursor()
