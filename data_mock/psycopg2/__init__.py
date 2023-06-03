from collections import OrderedDict

from data_mock.exceptions import InvalidMockData
import data_mock.mock_helpers.provider as provider

class Cursor:

    def __init__(self, cursor_factory = None, mock_data = None, use_dict = False, *args, **kwargs):
        self.data_provider = provider.ProvideData()
        if mock_data:
            self.data_provider.add_data(data = mock_data, tag = 'default')
        self.register_initial_mock_data()
        self.use_dict = use_dict


    def mock_set_cursor_factory(self, cursor_factory):
        if hasattr(cursor_factory, 'row_factory'):
            self.use_dict = True
        else:
            raise InvalidMockData('not sure what to do with cursor')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def execute(self, query, mock_data = None):
        """
        all args ignored except query
        """

        key = self._get_sql_key(query)
        if key:
            self.data, self.meta_data = self.data_provider.get_data(key)
            if not data:
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

    def _construct_tuple_row(self, row):
        new_row = []
        for data_obj in row:
            new_row.append(data_obj.value)
        return tuple(new_row)

    def _construct_orrderd_dict_row(self, row):
        od = OrderedDict()
        for data_obj in row:
            od[data_obj.name] = data_obj.value
        return od

    def fetchmany(self, n):
        counter = 0
        final = []
        if not self.data:
            return
        for counter, row in enumerate(self.data):
            if not self.use_dict:
                new_row = self._construct_tuple_row(row)
                final.append(new_row)
            else:
                new_row = self._construct_orrderd_dict_row(row)
                final.append(new_row)
            if counter + 1 == n:
                return final
        return final

    def _get_sql_key(self, query:str)-> str:
        for line in query.split('\n'):
            if 'py-bigquery-mock-register:' in line:
                fields = line.split(':')
                if len(fields) != 2:
                    raise exceptions.InvalidMockData('hint should be in format "py-bigquery-mock-register: key"')
                return fields[1].strip()
class Connect:

    def __init__(self, dsn=None, connection_factory=None, 
            mock_data = None,  **kwargs):
        self.cursor_class = Cursor()
        if mock_data:
            self.cursor_class.data_provider.add_data(data = mock_data, tag = 'default')
        

    def register_initial_mock_data(self):
        pass

    def register_mock_data(self, key, mock_data):
        self.cursor_class.data_provider.add_data(data = mock_data, tag = key)

    def cursor(self, cursor_factory = None,  *args, **kwargs):
        if cursor_factory:
            self.cursor_class.mock_set_cursor_factory(cursor_factory)
        return self.cursor_class

class connect(Connect):
    pass


def connect_(dsn=None, connection_factory=None, 
            cursor_factory=None,  **kwargs):
    return MockCursor()
