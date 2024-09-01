import sys
import os

from unittest import mock
from google.cloud import bigquery

def get_days(start_date: str, end_date: str)-> object:
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
    return rows

def caclulate_minutes(start_date: str, end_date: str)-> int:
    rows = get_days(
            start_date = start_date,
            end_date = end_date
            )
    minutes= None
    for i in rows:
        minutes = i.minutes
    if minutes == None:
        return 0
    return  int(minutes/(60 *24))

#====================TEST STARTS HERE===================


def mock_rows1(*args, **kwargs):

    class Mock:

        def __init__(self):
            self.minutes = 6686876
    return [Mock()]

class MockClient1():

    def query(self, query, *args, **kwargs):
        return self

    def result(self, *args, **kwargs):
        class Mock:

            def __init__(self, minutes):
                self.minutes = minutes
        return [Mock(minutes = 6686876)]

@mock.patch(__name__ + '.get_days', side_effect= mock_rows1 )
def test_calulate_mock_func(m1):
    result  = caclulate_minutes(
            start_date = '2023-01-01',
            end_date = '2024-01-01'
            )

    assert result == 4643

@mock.patch('google.cloud.bigquery.Client', side_effect= MockClient1 )
def test_calulate_mock_class(m1):
    result  = caclulate_minutes(
            start_date = '2023-01-01',
            end_date = '2024-01-01'
            )

    assert result == 4643
