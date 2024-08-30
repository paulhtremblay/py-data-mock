from google.cloud import bigquery

from unittest import mock
import data_mock.gcp.client as client
import data_mock.gcp.table as table


def create_table():
    client = bigquery.Client()
    schema=[ 
            bigquery.SchemaField('date', 'DATE', mode='REQUIRED'),
            bigquery.SchemaField('field_one', 'STRING', mode='NULLABLE'),
            bigquery.SchemaField('field_two', 'INTEGER', mode='NULLABLE'),
            ]
    dataset_ref = client.dataset('data_engineering')
    table_ref = dataset_ref.table('example_table')
    table = bigquery.Table(table_ref, schema=schema) #problem here
    partition_field = '_PARTITIONTIME'
    table.clustering_fields = ['date']
    table.description = 'an example table'
    table.time_partitioning = bigquery.Table.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY, 
                require_partition_filter=True)
        
    table_result = client.create_table(table)  
    print(table_result.table_id)

#====================TEST STARTS HERE===================

class MockClient1(client.Client):
    pass

class MockTable1(table.Table):
    pass

@mock.patch('google.cloud.bigquery.Client', side_effect= MockClient1 )
@mock.patch('google.cloud.bigquery.Table', side_effect= MockTable1 )
def test_create_table(m1, m2):
    create_table()

#create_table()
