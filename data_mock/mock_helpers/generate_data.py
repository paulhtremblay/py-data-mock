import string
import random

import functools
import inspect

from decimal import *
import datetime
from datetime import timezone
from datetime import timedelta


import types

from data_mock.google.cloud.bigquery import SchemaField
from data_mock.mock_helpers.provider import Data

def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

def generate_none(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_ = get_default_args(func)
        if (kwargs.get('make_none')  or args_['make_none']) and random.randint(1,100) <= args[0].percent_nullable:
            return None
        return func(*args, **kwargs)
    return wrapper


class MakeMockDataBase:

    def __init__(self):
        self.string_length = 7
        self.start_float = 1
        self.end_float = 10
        self.start_int = 1
        self.end_int = 10
        self.date_start = datetime.datetime(1900,1,1)
        self.date_end = datetime.datetime(2023,1,1)
        self.percent_nullable = 30

    @generate_none
    def make_string(self, make_none = False):
        return ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=self.string_length))

    @generate_none
    def make_int(self, make_none = False):
        return random.randint(self.start_int,self.end_int)

    @generate_none
    def make_float(self, make_none = False):
        return random.uniform(self.start_float, self.end_float)

    @generate_none
    def make_decimal(self, make_none = False):
        return Decimal(random.randint(self.start_int, self.end_int))

    @generate_none
    def make_boolean(self, make_none = False):
        return random.choice([True, False])

    @generate_none
    def make_timestamp(self, make_none = False):
        return  datetime.datetime(2022,1,1, tzinfo = timezone.utc)

    @generate_none
    def make_datetime(self, make_none = False):
        delta = self.date_end - self.date_start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return self.date_start + timedelta(seconds=random_second)

    @generate_none
    def make_date(self, make_none = False):
        return self.make_datetime().date()

    @generate_none
    def make_time(self, make_none = False):
        return self.make_datetime().time()

class MakeMockBQData(MakeMockDataBase):

    def __init__(self):
        super().__init__()

    def make_STRING(self, name:str = None, mode:str = None) -> str:
        return self.make_string(make_none = mode == 'NULLABLE')

    def make_BYTES(self, name:str = None, mode:str = None) -> bytes:
        return self.make_string().encode('utf8')

    def make_INT64(self, name:str = None, mode:str = None) -> int:
        return self.make_int()

    def make_FLOAT(self, name:str = None, mode:str = None) -> float:
        return self.make_float()

    def make_FLOAT64(self, name:str = None, mode:str = None) -> float:
        return self.make_float()

    def make_NUMERIC(self, name:str = None, mode:str = None) -> str:
        return self.make_decimal()

    def make_BIGNUMERIC(self, name:str = None, mode:str = None) -> str:
        return self.make_decimal()

    def make_BOOLEAN(self, name:str = None, mode:str = None) -> str:
        return self.make_boolean()

    def make_BOOL(self, name:str = None, mode:str = None) -> str:
        return self.make_boolean()

    def make_GEOGRAPHY(self, name:str = None, mode:str = None) -> str:
        raise NotImplementedError()

    def make_TIMESTAMP(self, name:str = None, mode:str = None) -> str:
        return self.make_timestamp()

    def make_DATE(self, name:str = None, mode:str = None) -> str:
        return self.make_date()

    def make_TIME(self, name:str = None, mode:str = None) -> str:
        return self.make_time()

    def make_DATETIME(self, name:str = None, mode:str = None) -> str:
        return self.make_datetime()

O = MakeMockBQData()
CONVERT_DICT = {
        'STRING': O.make_STRING,
        'DATE': O.make_DATE,
        'INTEGER': O.make_INT64
        }

def generate_value(name, field_type, mode):
    method = CONVERT_DICT[field_type]
    return method(name = name, mode = mode)

def generate_field(f:SchemaField) -> dict:
    final = {f.name:None}
    stack = [(f, f.name, final)]
    while stack:
        current = stack.pop()
        current_o = current[0]
        current_name = current[1]
        if len(current_o.fields) != 0:
            current[2][current_name] = []
            for i in current_o.fields[0]:
                temp = {i.name:None}
                current[2][current_name].append(temp)
                stack.append((i, i.name, temp))
        else:
            current[2][current_name] = generate_value(field_type = current_o.field_type,
                    name = current_o.name, mode = current_o.mode)
    return final

def convert_dict_to_list(data):
    #not used
    new_l = []
    stack = [{'data':data,  'append_to' : new_l}]
    counter = 0
    while len(stack) != 0:
        stack_info = stack.pop()
        stack_data = stack_info['data']
        append_to = stack_info['append_to']
        for n, i in enumerate(stack_data):
            assert isinstance(i, dict)
            for key in i.keys():
                value = i[key]
                if not isinstance(value, list):
                    append_to.append((key, value))
                else:
                    append_to.append([key])
                    stack.append({'data': value, 'append_to' : append_to[-1]})
    return new_l

def generate_data(schema:list, num_rows:int = 1) -> types.GeneratorType:
    for i in range(num_rows):
        l = []
        for j in schema:
            r = generate_field(j)
            for key in r.keys():
                l.append(Data(name = key,value = r[key]))
        yield l

class GenerateDataFromSchema:

    def __init__(self, num_rows, schema):
        mock_bq = MakeMockBQData()
        self.convert_dict = {
                'STRING': mock_bq.make_STRING,
                'DATE': mock_bq.make_DATE,
                'INTEGER': mock_bq.make_INT64
                }
        self.num_rows = num_rows
        self.schema = schema

    def generate_field(self, f:SchemaField) -> dict:
        """
        simple case: {field: STRING}, in which case, the stack is 
        and remains 1,and only else is executed

        recursive case: {field: fields[]}, in which case, fields is 
        added to to the stack as a list of dicts. If all of these dicts
        are simple and have no fields, then the stack is exhausted. Otherwise,
        the stack is added to, and so on
        """
        final = {f.name:None}
        stack = [(f, f.name, final)]
        while stack:
            current = stack.pop()
            current_o = current[0]
            current_name = current[1]
            if len(current_o.fields) != 0:
                current[2][current_name] = []
                for i in current_o.fields[0]:
                    temp = {i.name:None}
                    current[2][current_name].append(temp)
                    stack.append((i, i.name, temp))
            else:
                current[2][current_name] = generate_value(field_type = current_o.field_type,
                        name = current_o.name, mode = current_o.mode)
        return final

    def generate_data(self) -> types.GeneratorType:
        for i in range(self.num_rows):
            l = []
            for j in self.schema:
                r = self.generate_field(j)
                for key in r.keys():
                    l.append(Data(name = key,value = r[key]))
            yield l

    def generate_value(self, name, field_type, mode):
        method = self.convert_dict[field_type]
        return method(name = name, mode = mode)

    def query_results(self):
        return self.generate_data(), {'total_rows':self.num_rows}
