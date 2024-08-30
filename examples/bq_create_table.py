from google.cloud import bigquery

from unittest import mock
import data_mock.gcp.client as client
import data_mock.gcp.table as table
import data_mock.gcp.bigquery as bigqueryT


def create_table():
    client = bigquery.Client()
    schema=[ 
            bigquery.SchemaField('date', 'DATE', mode='REQUIRED'),
            bigquery.SchemaField('field_one', 'STRING', mode='NULLABLE'),
            bigquery.SchemaField('field_two', 'INTEGER', mode='NULLABLE'),
            ]

    table = bigquery.Table(table_ref = 'paul-henry-tremblay.data_engineering.example_table', schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        )
    table.require_partition_filter = True
    table.clustering_fields = ['date']
    table.description = 'an example table'
    table = client.create_table(table) 
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )
    print(f'part is {table.time_partitioning}')
    print(dir(table.time_partitioning))
    print(table.time_partitioning.type_)
    print(table.partitioning_type)

#====================TEST STARTS HERE===================

class MockClient1(client.Client):
    pass

class MockTable1(table.Table):
    pass

class MockBq(bigqueryT.TimePartitioning):
    pass


@mock.patch('google.cloud.bigquery.Client', side_effect= MockClient1 )
@mock.patch('google.cloud.bigquery.Table', side_effect= MockTable1 )
@mock.patch('google.cloud.bigquery.TimePartitioning', side_effect= MockBq )
def test_create_table(m1, m2, m3):
    create_table()

DEBUG=False
if DEBUG:
    client = bigquery.Client()
    table_ref = 'paul-henry-tremblay.data_engineering.example_table'
    client.delete_table(table_ref, 
            not_found_ok=True)
    create_table()
