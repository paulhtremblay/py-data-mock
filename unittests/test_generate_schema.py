import sys
sys.path.append('.')

import unittest
from data_mock.google.cloud.bigquery import SchemaField
from data_mock.mock_helpers import generate_data
from data_mock.google.cloud import bigquery

SCHEMA = [SchemaField(
                'jobs', 'RECORD', 'REPEATED', fields = (
                (SchemaField('duration', 'INTEGER', 'NULLABLE', None, None, (), None), 
                SchemaField('date', 'DATE', 'NULLABLE', None, None, (), None)), None)), 
            SchemaField('addresses', 'STRING', 'REPEATED', None, None, (), None), 
            SchemaField('name', 'STRING', 'NULLABLE', None, None, (), None)]

SCHEMA2 = [SchemaField(
                'jobs', 'RECORD', 'REPEATED', fields = (
                    (SchemaField('duration', 'INTEGER', 'NULLABLE'), 
                    SchemaField('date', 'DATE', 'NULLABLE'),
                    SchemaField('data', 'DATE', 'REPEATED', 
                        fields = (
                            (SchemaField('data2', 'DATE', 'NULLABLE'), 
                            ),)
                        ),
                )
                    ,),
                ), 
            SchemaField('addresses', 'STRING', 'REPEATED', None, None, (), None), 
            SchemaField('name', 'STRING', 'NULLABLE', None, None, (), None)]

class TestGenearteData(unittest.TestCase):

    def test_generate_data_gets_correct_values(self):
        gen_from_schema = generate_data.GenerateDataFromSchema(num_rows = 1, schema = SCHEMA2)
        all_names = []
        jobs = None
        for i in gen_from_schema.generate_data():
            for j in i:
                all_names.append(j.name)
                if j.name == 'jobs':
                    jobs = j.value
        self.assertEqual(all_names, ['jobs', 'addresses', 'name'])

    def test_generate_data_gets_correct_values2(self):
        gen_from_schema = generate_data.GenerateDataFromSchema(num_rows = 10, schema = SCHEMA2)
        gen, metadata = gen_from_schema.query_results()
        for n, row in enumerate(gen):
            for item in row:
                self.assertTrue(hasattr(item, 'name'))
                self.assertTrue(hasattr(item, 'value'))
        self.assertEqual(n, 10 -1)

    def test_generate_fake_data_with_register(self):
        gen_from_schema = generate_data.GenerateDataFromSchema(num_rows = 10, schema = SCHEMA2)

        class Client(bigquery.Client):

            def register_initial_mock_data(self):
                self.data_provider.add_data(data =gen_from_schema, tag = 'default')
        client = Client()
        r = client.query(query = '')
        for n, i in enumerate(r):
            for j in i.items():
                self.assertEqual(len(j), 2)
        self.assertEqual(n +1, 10)



if __name__ == '__main__':
    unittest.main()
