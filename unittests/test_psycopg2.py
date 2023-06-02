import sys

from collections.abc import Iterable 

sys.path.append('.')
import unittest

import data_mock.psycopg2
import data_mock.psycopg2.extras

class TestResults(unittest.TestCase):

    def setUp(self):
        pass

    def  tearDown(self):
        pass

    def test_connections_has_methods(self):
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x')
        self.assertTrue(hasattr(connection, 'cursor'))
        c = connection.cursor()

    def test_fetch_with_one_row(self):
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x')
        cursor = connection.cursor()
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        cursor.execute(query = 'some query', mock_data = mock_data)
        while True:
            rows = cursor.fetchmany(2000)
            if not rows:
                break
            else:
                for i in rows:
                    pass

    def test_fetch_with_two_row(self):
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x')
        cursor = connection.cursor()
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
        [('field3', 'value3'), ('field4', 'value4')],
            ]
        cursor.execute(query = 'some query', mock_data = mock_data)
        while True:
            rows = cursor.fetchmany(1)
            if not rows:
                break
            else:
                for i in rows:
                    print(i)
                    pass

    def test_dict_cursor(self):
        sql = "some query"
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x')
        with connection.cursor(
                cursor_factory = data_mock.psycopg2.extras.RealDictCursor
                ) as cursor:
            cursor.execute(sql)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    break

if __name__ == '__main__':
    unittest.main()
