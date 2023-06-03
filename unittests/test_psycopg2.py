import sys

from collections.abc import Iterable
from collections import OrderedDict

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
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x', mock_data = mock_data)
        cursor = connection.cursor()
        cursor.execute(query = 'some query')
        number_rows = 0
        while True:
            rows = cursor.fetchmany(2000)
            if not rows:
                break
            else:
                for i in rows:
                    number_rows += 1
        self.assertEqual(number_rows, 1)

    def test_fetch_with_two_row(self):
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
        [('field3', 'value3'), ('field4', 'value4')],
            ]
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x', mock_data = mock_data)

        cursor = connection.cursor()
        cursor.execute(query = 'some query')
        number_rows = 0
        while True:
            rows = cursor.fetchmany(1)
            if not rows:
                break
            else:
                for i in rows:
                    self.assertTrue(isinstance(i, tuple))
                    number_rows += 1
        self.assertEqual(number_rows, 2)

    def test_dict_cursor(self):
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        sql = "some query"
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x', mock_data = mock_data)
        number_rows = 0
        with connection.cursor(
                cursor_factory = data_mock.psycopg2.extras.RealDictCursor
                ) as cursor:
            cursor.execute(sql)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    number_rows += 1
                    self.assertTrue(isinstance(row, OrderedDict))
        self.assertEqual(number_rows, 1)

if __name__ == '__main__':
    unittest.main()
