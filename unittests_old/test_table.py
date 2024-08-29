import sys
sys.path.append('.')
import unittest

from data_mock.google.cloud.bigquery import Client
from data_mock.google.cloud.bigquery import InvalidMockData
from data_mock.google.cloud.bigquery import Table
from data_mock.google.cloud.bigquery import SchemaField
from data_mock.google.cloud.bigquery import DatasetReference
from data_mock.google.cloud.bigquery import TableReference
from data_mock.google.cloud.bigquery import TimePartitioning
from data_mock.google.cloud.bigquery import TimePartitioningType


class TestTable(unittest.TestCase):

    def test_create_table_obj_with_dataset_ref(self):
        dataset_ref = DatasetReference(project = 'mock', dataset_id = 'mock')
        table_ref = TableReference(dataset_ref = dataset_ref, table_id = 'x')
        t = Table(table_ref = table_ref)

    def test_create_table_obj_with_str(self):
        t = Table(table_ref = 'mock.mock.mock')

    def test_timepartitioningDAY(self):
        type_=TimePartitioningType.DAY

    def test_timepartitioningHOUR(self):
        type_=TimePartitioningType.HOUR

    def test_timepartitioningMONTH(self):
        type_=TimePartitioningType.MONTH

    def test_not_valid_syntax_for_table_creation_without_create(self):
        table = Table(table_ref = 'mock.mock.mock')
        day = TimePartitioningType.DAY
        table.time_partitioning = TimePartitioning(type_ = day,
                field = 'string from schema'
                )

    def test_not_valid_syntax_for_table_creation_with_create(self):
        table = Table(table_ref = 'mock.mock.mock')
        day = TimePartitioningType.DAY
        table.time_partitioning = TimePartitioning(type_ = day,
                field = 'string from schema'
                )
        client = Client(project = 'mock')

        table = client.create_table(table)

if __name__ == '__main__':
    unittest.main()

