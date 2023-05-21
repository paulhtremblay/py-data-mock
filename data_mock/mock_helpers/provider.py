import types
class Data:

    def __init__(self, name, value):
        self.name = name
        self.value = value


class ProvideData:

    def __init__(self):
        self.dict = {}

    def data_from_list(self, data:[[]], tag:str) -> types.GeneratorType:
        def my_func():
            for i in data:
                temp = []
                for j in i:
                    c = Data(name = j[0], value = j[1])
                    temp.append(c)
                yield temp
        self.dict[tag] = my_func

    def add_data(self, data:[list], tag:str):
        if isinstance(data, list):
            self.data_from_list(data, tag)
            return
        self.dict[tag] = data

    def get_data(self, key:str) -> [None, types.GeneratorType]:
        if not self.dict.get(key):
            return None
        assert  hasattr(self.dict[key], '__call__')
        g = self.dict[key]()
        for i in g:
            yield i
