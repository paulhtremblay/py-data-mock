# py-data-mock

pip install py-data-mock

BigQuery
=========

Simple Example
--------------
==============

```python

import  data_mock.google.cloud.bigquery  as bigquery

SQL = "Any string, since we are mocking"
bigquery_client = bigquery.Client()
result = bigquery_client.query(SQL)
for i in result: #loop will never be entered, since no data was registered
    pass
```

Register Data
-------------

```python

bigquery_client = bigquery.Client(
    mock_data = [
        [('field', 'value')],
    ]
                                  )
result = bigquery_client.query(SQL)
print(f'total rows are {result.total_rows}')
for i in result: 
    field_value = i.get('field')
    print(f'field_value is {field_value}')
```

As Subclass
------------
```python

class Client(bigquery.Client):

    def __init__(self):
        mock_data = [
                [('field', 'value')
                    ]
                ]
        super().__init__(mock_data = mock_data)

bigquery_client = Client()
result = bigquery_client.query(SQL)
print(f'total rows are {result.total_rows}')
for i in result: 
    field_value = i.get('field')
    print(f'field_value is {field_value}')
```

Register Data for Each SQL
--------------------------

You can register results for different queries. In the comment section of the SQL, put:
``` py-bigquery-mock-register: <tag> ```


```python
bigquery_client = bigquery.Client()

SQL="""
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

mock_data =[   
            [   ('name', '10th & Red River'),
                ('status', 'active'),
                ('address', '699 East 10th Street')],
            [   ('name', '11th & Salina'),
                ('status', 'active'),
                ('address', '1705 E 11th St')]]


bigquery_client.register_mock_data(key = 'bikeshare-name-status-address', 
        mock_data = mock_data)

result1 = bigquery_client.query(query = "SELECT * FROM `bigquery-public-data.austin_bikeshare.bikeshare_stations`"
)
for i in result1:
    print('nothing found, because data not registered')
result2 = bigquery_client.query(query = SQL)
for i in result2:
    for j in i.items():
        print(j)
```

Custom Classes to Provide Data
-------------------------------

A class can be used to provide results to a query. The class below will return no data with the first call, but data on the second call.
The class must provide a method `query_results`, and this method must returns two objects: a generator, and a dictionary of metadata.


```python
class ProviderData1:

    def __init__(self):
        self.__call_no = 0

    def gen_func1(self):
        for i in range(10):
            yield [provider.Data(name = 'field', value = i)]

    def gen_func2(self):
        return 
        yield

    def query_results(self):
        self.__call_no += 1
        if self.__call_no == 1:
            return self.gen_func2(), {'total_rows':0}
        else:
            return self.gen_func1(), {'total_rows':10}


client = bigquery.Client(mock_data = ProviderData1())
sql = "SELECT * FROM table"
result1 = client.query(query = sql)
self.assertEqual(result1.total_rows, 0)
#loop should not be entered
for i in result1:
    assert False
result2 = client.query(query = sql)
self.assertEqual(result2.total_rows, 10)
for i in result2:
    for j in i.items():
        self.assertEqual(j, ('field', 0))
    break

```
Storage
========

```python
from data_mock.google.cloud import storage
storage_client = storage.Client()
bucket = storage_client.bucket('bucket_name')
blob = bucket.blob('blob_name')
blob.upload_from_string(data= 'string', content_type='application/json')  
```
