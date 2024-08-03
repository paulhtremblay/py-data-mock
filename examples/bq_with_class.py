import sys
import os
dirname = os.path.dirname(os.path.abspath(__file__))
one_up = os.path.split(dirname)[0]
sys.path.append(one_up)

from unittest import mock
import data_mock.gcp.client as client
from google.cloud import bigquery

def get_mb(id_:int)-> int:
    client = bigquery.Client()
    sql = f"""
    SELECT  SUM(bytes) as bytes
FROM
  `paul-henry-tremblay.data_engineering.tv_streaming`
where id = {id_}
    """
    query_job = client.query(sql)
    rows = query_job.result() 
    the_bytes= None
    for i in rows:
        the_bytes = i.bytes
        i.bytes
    if the_bytes == None:
        return 0
    return  .000001 * the_bytes

#====================TEST STARTS HERE===================

class MockClient1(client.Client):

    def query(self, query):
        return self.run_query(data = [[('bytes', 1)]], m = {})

class MockClient2(client.Client):
    pass


@mock.patch('google.cloud.bigquery.Client', side_effect= MockClient1 )
def test_get_mb1(m1):
    result  = get_mb(1)
    assert result == 1e-06

@mock.patch('google.cloud.bigquery.Client', side_effect= MockClient2 )
def test_get_mb1(m1):
    result  = get_mb(1)
    assert result == 0

