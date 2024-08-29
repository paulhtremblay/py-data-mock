import sys
import os
dirname = os.path.dirname(os.path.abspath(__file__))
one_up = os.path.split(dirname)[0]
sys.path.append(one_up)

from unittest import mock
import data_mock.gcp.client as client
from google.cloud import bigquery

def get_days(start_date: str, end_date: str)-> int:
    client = bigquery.Client()
    sql = f"""
    SELECT SUM(duration_minutes) AS minutes
FROM
  `bigquery-public-data.austin_bikeshare.bikeshare_trips`
WHERE start_time >= '{start_date}'
AND start_time < '{end_date}'
    """
    query_job = client.query(sql)
    rows = query_job.result() 
    minutes= None
    for i in rows:
        minutes = i.minutes
    if minutes == None:
        return 0
    return  int(minutes/(60 *24))

#====================TEST STARTS HERE===================

class MockClient1(client.Client):

    def query(self, query):
        return self.run_query(data = [[('minutes', 6686876)]], m = {})

class MockClient2(client.Client):
    pass

@mock.patch('google.cloud.bigquery.Client', side_effect= MockClient1 )
def test_get_days_rturns_right_value(m1):
    result  = get_days(
        start_date = '2023-01-01',
        end_date = '2024-01-01'
        )
    assert result == 4643

@mock.patch('google.cloud.bigquery.Client', side_effect= MockClient2 )
def test_get_days_out_of_range_returns_0(m1):
    result  = get_days(
            start_date = '1900-01-01', 
            end_date = '1901-01-01')
    assert result == 0

