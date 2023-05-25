import sys
sys.path.append('.')

import unittest

from data_mock.google.cloud import bigquery

class TestResults(unittest.TestCase):

    def setUp(self):
        pass

    def  tearDown(self):
        pass

    def test_config_succeeds(self):
        client = bigquery.Client()
        job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("id", "INTEGER"),
            bigquery.SchemaField("users", field_type='RECORD', mode='REPEATED',
                fields=[
                    bigquery.SchemaField("date", "TIMESTAMP"),
                ]
            ),
        ],
        autodetect=True,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND, 
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )
        

    def test_load_job_from_uri(self):
        table_id = 'mock-table-id'
        client = bigquery.Client()
        uri = f"gs://uri"
        job_config = bigquery.LoadJobConfig()

        load_job = client.load_table_from_uri(
            source_uris = uri,
            destination = table_id ,
            location="US",
            job_config=job_config,
        )
        load_job.result()
        destination_table = client.get_table(table_id)
        self.assertTrue(hasattr(destination_table, 'table_id'))
        self.assertTrue(hasattr(destination_table, 'dataset_id'))
        self.assertTrue(hasattr(destination_table, 'num_rows'))
        self.assertTrue(hasattr(destination_table, 'project'))

if __name__ == '__main__':
    unittest.main()
