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



def generate_data(schema, num_rows = 1):
    for i in range(num_rows):
        temp = []
        temp2 = []
        for j in schema:
            r = generate_field(j)
            temp.append(r)
            for key in r.keys():
                temp2.append(Data(name = key,value = r[key]))
        yield temp2
