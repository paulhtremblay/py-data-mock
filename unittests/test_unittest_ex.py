import json
import uuid
import datetime

import unittest
from unittest import mock

from google.cloud import storage
from google.cloud import bigquery

from data_mock.google.cloud import storage as mock_storage
from data_mock.google.cloud import bigquery as bigquery_mock

import pprint
pp = pprint.PrettyPrinter(indent=4)

#=======================================
#Code to Test
#=======================================

def store_matchpoint_data(data: dict, bucket_name: str = 'a-test-bucket-dev',  
            verbose: bool=False) -> str:
    """
    uploads a dictionary as JSON to a bucket as an arbritrary UUID and returns the UUID
    """
    blob_name = uuid.uuid4().hex
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name = bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(data=json.dumps(data),content_type='application/json')  
    if verbose:
        print(blob_name, data)
    return blob_name

def records_are_active():
    client = bigquery.Client(project= 'project')
    sql =  """
            /*
            py-bigquery-mock-register: bikeshare-name-status-address

            */
        SELECT
      name, status, address
    FROM
      `bigquery-public-data.austin_bikeshare.bikeshare_stations`
      order by name, status, address
    LIMIT
      2
        """
    row_iter = client.query(sql).result()
    assert row_iter.total_rows  == 2
    for i in row_iter:
        if i.get('status') != 'active':
            return False
    return True

def first_result():
    client = bigquery.Client(project= 'sbgtv-data-platform-dev')
    sql =  """
        SELECT
      name, status, address
    FROM
      `bigquery-public-data.austin_bikeshare.bikeshare_stations`
      order by name, status, address
    LIMIT
      2
        """
    row_iter = client.query(sql).result()
    assert row_iter.total_rows  == 2
    for i in row_iter:
        first = i.get('name')
        break
    return first
    

def does_name_exist():
    client = bigquery.Client(project= 'project')
    sql =  """
        SELECT
      name, status, address
    FROM
      `bigquery-public-data.austin_bikeshare.bikeshare_stations`
      where name = '132a7346f9ca11edb43b7aa6114393d9'
      order by name, status, address
    LIMIT
      2
        """
    row_iter = client.query(sql).result()
    return row_iter.total_rows != 0

def is_data_old():
    client = bigquery.Client(project= 'project')
    sql = """
    SELECT
       MAX(modified_date) AS max_date
      FROM
        `bigquery-public-data.austin_bikeshare.bikeshare_stations`

    """
    row_iter = client.query(sql).result()
    for i in row_iter:
        max_date = i.get('max_date')
        break
    diff = datetime.datetime.now() - max_date
    if diff.days> 100:
        return True

#============================
# Mocks
#============================

class MockClient1(bigquery_mock.Client):
    mock_data_ = [   [   ('name', '10th & Red River'),
        ('status', 'active'),
        ('address', '699 East 10th Street')],
    [   ('name', '11th & Salina'),
        ('status', 'active'),
        ('address', '1705 E 11th St')]]

    def __init__(self, project = None, mock_data = None, 
            mock_list_of_tables = None):
        super().__init__(mock_data = mock_data)
        self._data_provider.add_data(data = self.mock_data_, tag = 'bikeshare-name-status-address')

class MockClient2(bigquery_mock.Client):
    mock_data_ = [   [   ('name', '10th & Red River'),
        ('status', 'active'),
        ('address', '699 East 10th Street')],
    [   ('name', '11th & Salina'),
        ('status', 'active'),
        ('address', '1705 E 11th St')]]

    def __init__(self, project = None, mock_data = None, 
            mock_list_of_tables = None):
        super().__init__(mock_data = mock_data)
        self._data_provider.add_data(data = self.mock_data_, tag = 'default_')

class MockClient3(bigquery_mock.Client):
    mock_data_ = [  [  ('max_date', datetime.datetime(2022, 3, 4, 10, 38, 0)),]]
    def __init__(self, project = None, mock_data = None, 
            mock_list_of_tables = None):
        super().__init__(mock_data = mock_data)
        self._data_provider.add_data(data = self.mock_data_, tag = 'default_')

def f(*args, **kwargs):

    mock_data = [   [   ('name', '10th & Red River'),
        ('status', 'active'),
        ('address', '699 East 10th Street')],
    [   ('name', '11th & Salina'),
        ('status', 'active'),
        ('address', '1705 E 11th St')]]
    client = bigquery_mock.Client()
    client.register_mock_data(key = 'bikeshare-name-status-address', 
        mock_data = mock_data)
    return client

#====================
# Test Suite
#====================

class TestGetData(unittest.TestCase):
    @mock.patch('google.cloud.storage.Client', side_effect= mock_storage.Client )
    def test_storage(self, mock_s):
        data = {'foo':'bar'}
        store_matchpoint_data(data = data) 


    @mock.patch('google.cloud.bigquery.Client', side_effect= f )
    def test_records_are_active_is_true1(self, bq_m):
        result = records_are_active()
        self.assertTrue(result)

    @mock.patch('google.cloud.bigquery.Client', side_effect= MockClient1 )
    def test_records_are_active_is_true2(self, bq_m):
        result = records_are_active()
        self.assertTrue(result)

    @mock.patch('google.cloud.bigquery.Client', side_effect= MockClient2 )
    def test_first_result_is_10th(self, bq_m):
        result = first_result()
        self.assertEqual(result, '10th & Red River')

    @mock.patch('google.cloud.bigquery.Client', side_effect= bigquery_mock.Client )
    def test_does_name_exist_returns_false(self, bq_m):
        result = does_name_exist()
        self.assertFalse(result)

    @mock.patch('google.cloud.bigquery.Client', side_effect= MockClient3 )
    def test_is_data_old_returns_true(self, bq_m):
        result = is_data_old()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
