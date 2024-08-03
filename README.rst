Py-data-mock
============

The library py-data-mock provides easy way to mock out data, with the focus on 
libraries for data engineering, such as BigQuery and requests. 

.. code:: python

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
         return self.run_query(
            data = [[('bytes', 1)]], 
            m = {}
            )

 class MockClient2(client.Client):
     pass
 
 @mock.patch('google.cloud.bigquery.Client', side_effect= MockClient1 )
 def test_get_mb1_returns_correct_value(m1):
     result  = get_mb(1)
     assert result == 1e-06

 @mock.patch('google.cloud.bigquery.Client', side_effect= MockClient2 )
 def test_get_mb1_no_value_returns_0(m1):
     result  = get_mb(1)
     assert result == 0

