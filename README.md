# py-data-mock

Simple Example
==============

```python

import  data_mock.google.cloud.bigquery  as bigquery

SQL = "Any string, since we are mocking"
bigquery_client = bigquery.Client()
result = bigquery_client.query(SQL)
for i in result: #loop will never be entered, since no data was registered
    pass
```

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

# as subclass

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
