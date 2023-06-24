import types
from typing import Union, List, Iterator, Type, Tuple, TypeVar
import data_mock.exceptions
from data_mock.google.cloud import bigquery
#from bigquery import SchemaField
import types

V = TypeVar('V')

class EmptyGenerator:
    #not used!

    def __init__(self):
        self.metadata = {}

    def gen_func(self):
        for i in range(0):
            yield i

    def query_results(self):
        return self.gen_func(), {'total_rows':0, 'schema' : None}

class QueryResultsFromList:

    def __init__(self, data:list):
        self.data = data
        self.make_schema()

    def make_schema(self) -> None :
        if len(self.data) == 0:
            self.schema = None
            return None
        schema = []
        for i in self.data[0]:
            schema.append(bigquery.SchemaField(name = i[0], field_type = str(type(i[1]))))
        self.schema = schema

    def gen_func(self) -> Iterator[List]:
        for i in self.data:
            l = []
            for j in i:
                c = Data(name = j[0], value = j[1])
                l.append(c)
            yield l

    def query_results(self):
        return self.gen_func(), {'total_rows':len(self.data), 'schema' : self.schema}

class Data:

    def __init__(self, name, value):
        self.name = name
        self.value = value


class ProvideData:

    def __init__(self):
        self.dict = {}

    def data_from_list(self, data:List, tag:str ):
        self._test_valid_data(data)
        self.dict[tag] = QueryResultsFromList(data = data)

    def add_data(self, data:Union[List, V], tag:str):
        if isinstance(data, list):
            self.data_from_list(data, tag)
        else:
            self.dict[tag] = data

    def get_data(self, key:str) -> Union[Tuple[None, None], Tuple[types.GeneratorType, dict]]:
        if not self.dict.get(key):
            return None, None
        if not  hasattr(self.dict[key], 'query_results'):
            raise data_mock.exceptions.InvalidMockData('object does not have query_results')
        if not isinstance(self.dict[key].query_results, types.MethodType):
            msg = '"query_results" is  not a method; did you pass the class rather than class()?'
            raise data_mock.exceptions.InvalidMockData(msg)
        return self.dict[key].query_results()

    def _test_valid_data(self, data):
        if not isinstance(data, list):
            raise data_mock.exceptions.InvalidMockData(f'{data} is not a list')
        errors = []
        for n, i in enumerate(data):
            if not isinstance(i, list):
                errors.append((n, i, 'not a list'))
        if len(errors) != 0:
            raise data_mock.exceptions.InvalidMockData(errors)

