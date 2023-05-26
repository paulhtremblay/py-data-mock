import types

from data_mock.google.cloud.bigquery import SchemaField
from data_mock.mock_helpers.provider import Data

def generate_value(field_type):
    return f'genearte for {field_type}'

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
            current[2][current_name] = generate_value(field_type = current_o.field_type)
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
