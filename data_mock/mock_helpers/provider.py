import types
import data_mock.exceptions

class Data:

    def __init__(self, name, value):
        self.name = name
        self.value = value


class ProvideData:

    def __init__(self):
        self.dict = {}

    def data_from_list(self, data:[[]], tag:str, metadata:dict = None) -> types.GeneratorType:
        self._test_valid_data(data)
        def my_func():
            for i in data:
                temp = []
                for j in i:
                    c = Data(name = j[0], value = j[1])
                    temp.append(c)
                yield temp
        self.dict[tag] = my_func, metadata

    def add_data(self, data:[list], tag:str, metadata: dict = None):
        if isinstance(data, list):
            self.data_from_list(data, tag)
            return
        self.dict[tag] = data, metadata

    def get_data(self, key:str) -> [None, types.GeneratorType]:
        if not self.dict.get(key):
            return None, None
        if not  hasattr(self.dict[key][0], '__call__'):
            raise data_mock.exceptions.InvalidMockData('not a function')

        g, metadata = self.dict[key]
        return g(), metadata

    def _test_valid_data(self, data):
        if not isinstance(data, list):
            raise data_mock.exceptions.InvalidMockData(f'{data} is not a list')
        errors = []
        for n, i in enumerate(data):
            if not isinstance(i, list):
                errors.append((n, i, 'not a list'))
        if len(errors) != 0:
            raise data_mock.exceptions.InvalidMockData(errors)

