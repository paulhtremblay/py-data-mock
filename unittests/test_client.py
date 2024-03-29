import sys
sys.path.append('.')
import unittest
from collections.abc import Iterable 

import datetime

from data_mock.google.cloud import bigquery
from data_mock.google.cloud.bigquery import SchemaField

#from data_mock.google.cloud.bigquery import QueryJobConfig
import data_mock.google.cloud.bigquery.table as _table
import  data_mock.google.cloud.bigquery.exceptions as _exceptions
import  data_mock.google.cloud.bigquery.schema as _schema
import data_mock.exceptions
import data_mock.mock_helpers.provider as provider


DATA1= [
        [('name', 'State Capitol @ 14th & Colorado'),
        ('status', 'closed'),
        ('address', '206 W. 14th St.')],
        [('name', 'Bullock Museum @ Congress & MLK'),
        ('status', 'closed'),
        ('address', '1881 Congress Ave.'),
        ]
]

def get_sql():
        return """
        SELECT
      name, status, address
    FROM
      `bigquery-public-data.austin_bikeshare.bikeshare_stations`
    LIMIT
      2
        """

def items_func_with_result_all(bq_client, sql):
    row_iter = bq_client.query(sql).result()
    final = []
    for i in row_iter:
        temp = []
        for j in i.items():
            temp.append(j)
        final.append(temp)
    return final

def items_func_with_result(bq_client, sql):
    row_iter = bq_client.query(sql).result()
    final = []
    for i in row_iter:
        for j in i.items():
            final.append(j)
        break
    return final

def items_func_not_use_result(bq_client, sql):
    row_iter = bq_client.query(sql)
    final = []
    for i in row_iter:
        for j in i.items():
            final.append(j)
        break
    return final

def get_func_no_key(bq_client, sql):
    row_iter = bq_client.query(sql)
    final = []
    for i in row_iter:
        final.append(i.get('name'))
    return final

def get_func_with_key(bq_client, sql):
    row_iter = bq_client.query(sql)
    final = []
    for i in row_iter:
        final.append(i.get('name'))
    return final

def get_func_with_key_with_result(bq_client, sql):
    row_iter = bq_client.query(sql).result()
    final = []
    for i in row_iter:
        final.append(i.get('name'))
    return final

def values_func_with_key_with_result(bq_client, sql):
    row_iter = bq_client.query(sql).result()
    final = []
    for i in row_iter:
        final.append(i.values())
    return final

def keys_func_with_key_with_result(bq_client, sql):
    row_iter = bq_client.query(sql).result()
    final = []
    for i in row_iter:
        final.append(i.keys())
    return final

class ProviderData1:

    def __init__(self):
        self.__call_no = 0

    def gen_func1(self):
        for i in range(10):
            yield [provider.Data(name = 'field', value = i)]

    def gen_func2(self):
        return 
        yield

    def query_results(self):
        self.__call_no += 1
        if self.__call_no == 1:
            return self.gen_func2(), {'total_rows':0}
        else:
            return self.gen_func1(), {'total_rows':10}

class BadClass1:
    def query_results(self):
        return None

class NestedClient1(bigquery.Client):
    def register_initial_mock_data(self):
        mock_data = [
                [
                    ('jobs', [{'duration': 3, 'date': datetime.date(2021, 1, 1)}]),
                    ('addresses', ['some address', 'some address 2']),
                    ('name', 'henry'),
                    ],
                [
                    ('jobs', [{'duration': 4, 'date': datetime.date(2021, 1, 3)}]),
                    ('addresses', ['some address2', 'some address 3']),
                    ('name', 'henry2'),
                    ]

                ]
        self.data_provider.add_data(data = mock_data, tag = 'default')

class GenClient(bigquery.Client):
    pass

class TestResults(unittest.TestCase):

    def setUp(self):
        pass

    def  tearDown(self):
        pass

    def test_items_first_result_returns_3_correct_name_values(self):
        client = bigquery.Client(mock_data = DATA1)
        f = items_func_with_result(bq_client = client, sql = get_sql())
        self.assertTrue(f[0], ('name', 'State Capitol @ 14th & Colorado'))
        self.assertTrue(f[1], ('status', 'closed'))
        self.assertTrue(f[2], ('address', '206 W. 14th St.'))

    def test_with_provider_class(self):
        client = bigquery.Client(mock_data = ProviderData1())
        sql = get_sql()
        result1 = client.query(query = sql)
        self.assertEqual(result1.total_rows, 0)
        #loop should not be entered
        for i in result1:
            assert False
        result2 = client.query(query = sql)
        self.assertEqual(result2.total_rows, 10)
        for i in result2:
            for j in i.items():
                self.assertEqual(j, ('field', 0))
            break

    def test_items_schema_has_correct_attributes(self):
        client = bigquery.Client(mock_data = DATA1)
        row_iter = client.query('').result()
        for i in row_iter.schema:
            self.assertTrue(hasattr(i, 'mode'))
            self.assertTrue(hasattr(i, 'name'))
            self.assertTrue(hasattr(i, 'field_type'))

    def test_items_first_result_not_using_result_method_returns_3_correct_name_values(self):
        client = bigquery.Client(mock_data = DATA1)
        f = items_func_not_use_result(bq_client = client, sql = get_sql())
        self.assertTrue(f[0], ('name', 'State Capitol @ 14th & Colorado'))
        self.assertTrue(f[1], ('status', 'closed'))
        self.assertTrue(f[2], ('address', '206 W. 14th St.'))

    def test_items_no_values_returns_empty_list(self):
        client = bigquery.Client()
        f = items_func_with_result(bq_client = client, sql = get_sql())
        self.assertEqual(f, [])

    def test_get_name_returns_2_correct_names(self):
        client = bigquery.Client(mock_data = DATA1)
        f = get_func_no_key(bq_client = client, sql = get_sql())
        self.assertEqual(f, ['State Capitol @ 14th & Colorado', 'Bullock Museum @ Congress & MLK'])
        
    def test_get_name_with_key_word_arg_returns_2_correct_names(self):
        client = bigquery.Client(mock_data = DATA1)
        f = get_func_with_key(bq_client = client, sql = get_sql())
        self.assertEqual(f, ['State Capitol @ 14th & Colorado', 'Bullock Museum @ Congress & MLK'])

    def test_get_name_with_key_word_arg_and_result_method_returns_2_correct_names(self):
        client = bigquery.Client(mock_data = DATA1)
        f = get_func_with_key_with_result(bq_client = client, sql = get_sql())
        self.assertEqual(f, ['State Capitol @ 14th & Colorado', 'Bullock Museum @ Congress & MLK'])

    def test_values_returns_2_correct_values(self):
        client = bigquery.Client(mock_data = DATA1)
        f = values_func_with_key_with_result(bq_client = client, sql = get_sql())
        self.assertEqual(f[0], ('State Capitol @ 14th & Colorado', 'closed', '206 W. 14th St.'))

    def test_keys_returns_correct_keys_first_result(self):
        client = bigquery.Client(mock_data = DATA1)
        f = keys_func_with_key_with_result(bq_client = client, sql = get_sql())
        self.assertTrue(list(f[0]), ['name', 'status', 'address'])

    def test_not_a_list_data_raises_InvalidData(self):
        client = bigquery.Client(mock_data = 1)
        self.assertRaises(
                data_mock.exceptions.InvalidMockData, 
                keys_func_with_key_with_result, 
                bq_client = client, 
                sql = get_sql()
                )

    def test_not_a_list_in_list_data_raises_InvalidData(self):
        data = [[('name', 'value',),], 1] 
        self.assertRaises(
                data_mock.exceptions.InvalidMockData, 
                bigquery.Client, mock_data = data
                 )
    def test_data_not_a_class_raises_InvalidData(self):
        class Client(bigquery.Client):

            def register_initial_mock_data(self):
                self.data_provider.add_data(data =ProviderData1, tag = 'default')
        client = Client()
        self.assertRaises(
                data_mock.exceptions.InvalidMockData, 
                client.query, query = ''
                 )

    def test_data_not_a_class2_raises_InvalidData(self):
        class Client(bigquery.Client):

            def register_initial_mock_data(self):
                self.data_provider.add_data(data =1, tag = 'default')
        client = Client()
        self.assertRaises(
                data_mock.exceptions.InvalidMockData, 
                client.query, query = ''
                 )

    def test_data_not_a_class3_raises_InvalidData(self):
        class Client(bigquery.Client):
            def query_results(self):
                return None

            def register_initial_mock_data(self):
                self.data_provider.add_data(data =BadClass1(), tag = 'default')

        c = Client()
        self.assertRaises(data_mock.exceptions.InvalidMockData,c.query, query = '')

    def test_data_not_registered_raises_InvalidData(self):
        client = bigquery.Client()
        sql = """

            py-bigquery-mock-register: data1
        """
        self.assertRaises(data_mock.exceptions.InvalidMockData,client.query, query = sql)


    def test_create_table_succeeds(self):
        table_id = 'project.dataset_id.tabele_id'
        schema = [
            _schema.SchemaField("full_name", "STRING", mode="REQUIRED"),
            _schema.SchemaField("age", "INTEGER", mode="REQUIRED"),
        ]
        client = bigquery.Client()
        table = _table.Table(table_ref = table_id, schema=schema)
        client.create_table(table)
        self.assertTrue(hasattr(table, 'project') and hasattr(table, 'table_id') and hasattr(table, 'dataset_id'))

    def test_create_table_as_string_succeeds(self):
        table_id = 'project.dataset_id.table_id'
        client = bigquery.Client()
        table = client.create_table(table = table_id)
        self.assertTrue(hasattr(table, 'project') and hasattr(table, 'table_id') and hasattr(table, 'dataset_id'))

    def test_register_data_reads_right_data(self):
        client = bigquery.Client()
        mock_data = [
            [('data1-test', 'found')],
            ]
        client.register_mock_data(key = 'data1', mock_data =mock_data)
        sql = """
            /*
            py-bigquery-mock-register: data1

            */
            SELECT 
            f FROM Table
            """
        f = items_func_with_result_all(bq_client = client, sql = sql)
        self.assertEqual(f, mock_data)

    def test_delete_table(self):
        client = bigquery.Client()
        client.delete_table(table = 'x.x.x', not_found_ok = True)

    def test_query_works_with_config(self):
        job_config = bigquery.QueryJobConfig(destination='mock-table-id')
        client = bigquery.Client(mock_data = DATA1)
        sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""

        query_job = client.query(sql, job_config=job_config)  

    def test_list_tables_returns_iterable(self):
        client = bigquery.Client(mock_data = DATA1)
        dataset_id = 'mock.mock'
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(isinstance(result, Iterable))

    def test_list_tables_returns_iterable_with_correct_obj(self):
        table = _table.Table(table_ref = 'proj.data.id')
        client = bigquery.Client(mock_list_of_tables = [table])
        dataset_id = 'mock.mock'
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(len(result) == 1)
        self.assertTrue(hasattr(result[0], 'table_id'))

    def test_list_delete_create_table(self):
        client = bigquery.Client()
        dataset_id = 'mock.mock'
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(len(result) == 0)
        table = client.create_table(table = 'x.x.x')
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(len(result) == 1)
        self.assertTrue(hasattr(result[0], 'table_id'))
        client.delete_table(table = 'x.x.x')
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(len(result) == 0)

    def test_list_delete_create_table_with_ref(self):
        client = bigquery.Client()
        dataset_id = 'mock.mock'
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(len(result) == 0)
        table = client.create_table(table = 'x.x.x')
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(len(result) == 1)
        self.assertTrue(hasattr(result[0], 'table_id'))
        client.delete_table(table = table)
        result = client.list_tables(dataset = dataset_id)
        self.assertTrue(len(result) == 0)

    def test_nested_1(self):
        client = NestedClient1()
        needed = [[{'duration': 3, 'date': datetime.date(2021, 1, 1)}], 
            [{'duration': 4, 'date': datetime.date(2021, 1, 3)}]]
        jobs_result = []
        address_result = []
        needed_address = [
                ['some address', 'some address 2'], 
                ['some address2', 'some address 3']
            ]

        result = client.query(query = '')
        for i in result:
            jobs_result.append(i.get('jobs'))
            address_result.append(i.get('addresses'))
        self.assertEqual(jobs_result, needed)
        self.assertEqual(needed_address, address_result)

    def test_nested_schema1(self):
        [SchemaField(
                'jobs', 'RECORD', 'REPEATED', None, None, 
                (SchemaField('duration', 'INTEGER', 'NULLABLE', None, None, (), None), 
                SchemaField('date', 'DATE', 'NULLABLE', None, None, (), None)), None), 
            SchemaField('addresses', 'STRING', 'REPEATED', None, None, (), None), 
            SchemaField('name', 'STRING', 'NULLABLE', None, None, (), None)]

    def test_nested_schema2(self):
        [SchemaField(
                'jobs', 'RECORD', 'REPEATED', fields = (
                (SchemaField('duration', 'INTEGER', 'NULLABLE', None, None, (), None), 
                SchemaField('date', 'DATE', 'NULLABLE', None, None, (), None)), None)), 
            SchemaField('addresses', 'STRING', 'REPEATED', None, None, (), None), 
            SchemaField('name', 'STRING', 'NULLABLE', None, None, (), None)]

    def test_get_table_has_att_num_rows(self):
        client = GenClient()
        destination_table = client.get_table('foo.bar.goo')
        self.assertTrue(hasattr(destination_table, 'num_rows'))

    def test_get_table_has_att_num_rows_no_dataset(self):
        client = GenClient()
        destination_table = client.get_table('goo')
        self.assertTrue(hasattr(destination_table, 'num_rows'))

if __name__ == '__main__':
    unittest.main()
