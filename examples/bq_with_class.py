from unittest import mock
import data_mock.gcp.bq_client as client
from google.cloud import bigquery

class TestClient1(client.Client):

    def query(self, query):
        return self.run_query(data = [[('bytes', 1)]], m = {})

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

def mock_client(*args, **kwargs):
    return TestClient1()

@mock.patch('google.cloud.bigquery.Client', side_effect= mock_client )
def test_get_mb1(m1):
    x = get_mb(1)
    print(x)

if __name__ == '__main__':
    test_get_mb1()
