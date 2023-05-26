import sys
sys.path.append('.')

import unittest
from data_mock.google.cloud.bigquery import SchemaField
from data_mock.mock_helpers import generate_data

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
        l = generate_data.generate_data(schema = SCHEMA2, num_rows = 1)
        all_names = []
        jobs = None
        for i in l:
            for j in i:
                all_names.append(j.name)
                if j.name == 'jobs':
                    jobs = j.value
        self.assertEqual(all_names, ['jobs', 'addresses', 'name'])


if __name__ == '__main__':
    unittest.main()
