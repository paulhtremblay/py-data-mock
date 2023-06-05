import sys

from collections.abc import Iterable
from collections import OrderedDict

sys.path.append('.')
import unittest

import data_mock.psycopg2
import data_mock.psycopg2.extras
from data_mock.psycopg2.exceptions import ProgrammingError
from data_mock.psycopg2.connect import Connect
from data_mock.psycopg2.cursor import Cursor
from data_mock.psycopg2.extras import RealDictCursor

class MockConnect1(Connect):

    def register_initial_mock_data(self):
        mock_data1 = [
        [('tag1', 'value1')],
            ]
        mock_data_default = [
        [('default', 'value1')],
            ]
        self.register_mock_data(key = 'tag1', mock_data = mock_data1)
        self.register_mock_data(key = 'default', mock_data = mock_data_default)

class MockCursor1(RealDictCursor):

    def register_initial_mock_data(self):
        mock_data1 = [
        [('tag1', 'value1')],
            ]
        mock_data_default = [
        [('default', 'value1')],
            ]
        self.register_mock_data(key = 'tag1', mock_data = mock_data1)
        self.register_mock_data(key = 'default', mock_data = mock_data_default)

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

    def test_fetch_with_one_row_returns_one_row(self):
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

    def test_fetch_with_two_row_returns_two_rows(self):
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

    def test_dict_cursor_returns_ordered_dict_and_one_row(self):
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

    def test_with_register_returns_correct_data(self):
        sql = """
        /*py-postgres-mock-register: tag1
        */
        """
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x')
        connection.register_mock_data(key = 'tag1', mock_data = mock_data)

        number_rows = 0
        with connection.cursor(
                cursor_factory = data_mock.psycopg2.extras.RealDictCursor
                ) as cursor:
            cursor.execute(sql)
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

    def test_no_execute_raises_error(self):
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x')
        with connection.cursor() as cursor:
            self.assertRaises(ProgrammingError, cursor.fetchmany, 100)

    def test_with_register_and_default_returns_corrct_num_rows(self):
        sql_tag1 = """
        /*py-postgres-mock-register: tag1
        */
        """
        sql_default = ''
        mock_data1 = [
        [('tag1', 'value1')],
            ]
        mock_data_default = [
        [('default', 'value1')],
            ]
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x', mock_data = mock_data_default)
        connection.register_mock_data(key = 'tag1', mock_data = mock_data1)

        with connection.cursor(
                cursor_factory = data_mock.psycopg2.extras.RealDictCursor
                ) as cursor:
            cursor.execute(sql_tag1)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('tag1' in row.keys())
            cursor.execute(sql_default)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('default' in row.keys())

    def test_with_register_with_class1(self):
        sql_tag1 = """
        /*py-postgres-mock-register: tag1
        */
        """
        sql_default = ''
        connection = MockConnect1( user='x', password='x', 
            host='x', port='x', database='x')

        with connection.cursor(
                cursor_factory = data_mock.psycopg2.extras.RealDictCursor
                ) as cursor:
            cursor.execute(sql_tag1)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('tag1' in row.keys())
            cursor.execute(sql_default)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('default' in row.keys())

    def test_fetch_with_one_row_initiate_cursor(self):
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        cursor = Cursor(mock_data = mock_data)
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

    def test_fetch_with_two_row_initaite_cursor(self):
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
        [('field3', 'value3'), ('field4', 'value4')],
            ]
        cursor = Cursor(mock_data = mock_data)
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

    def test_dict_cursor_has_ordered_dict_and_right_number_rowsiniitiate_cursor(self):
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        sql = "some query"
        number_rows = 0
        with RealDictCursor(
                mock_data = mock_data
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

    def test_with_register_returns_correct_data_initiate_cursor(self):
        cursorx = Cursor()
        sql = """
        /*py-postgres-mock-register: tag1
        */
        """
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        cursor = RealDictCursor()
        cursor.register_mock_data(key = 'tag1', mock_data = mock_data)

        number_rows = 0
        with cursor:
            cursor.execute(sql)
        with cursor:
            cursor.execute(sql)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    number_rows += 1
                    self.assertTrue(isinstance(row, OrderedDict))
        self.assertEqual(number_rows, 1)

    def test_no_execute_raises_error_initiate_cursor(self):
        cursor = Cursor()
        with cursor as cursor:
            self.assertRaises(ProgrammingError, cursor.fetchmany, 100)


    def test_with_register_and_default_returns_corrct_num_rows_initiate_cursor(self):
        sql_tag1 = """
        /*py-postgres-mock-register: tag1
        */
        """
        sql_default = ''
        mock_data1 = [
        [('tag1', 'value1')],
            ]
        mock_data_default = [
        [('default', 'value1')],
            ]
        cursor = RealDictCursor(mock_data = mock_data_default)
        cursor.register_mock_data(key = 'tag1', mock_data = mock_data1)

        with cursor:
            cursor.execute(sql_tag1)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('tag1' in row.keys())
            cursor.execute(sql_default)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('default' in row.keys())

    def test_with_register_with_class1_initiate_cursor(self):
        sql_tag1 = """
        /*py-postgres-mock-register: tag1
        */
        """
        sql_default = ''
        cursor = MockCursor1()

        with cursor:
            cursor.execute(sql_tag1)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('tag1' in row.keys())
            cursor.execute(sql_default)
            while True:
                rows = cursor.fetchmany(100)
                if not rows:
                    break
                for row in rows:
                    self.assertTrue('default' in row.keys())

    def test_fetch_with_one_row_returns_one_row_for_fetchall(self):
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x', mock_data = mock_data)
        cursor = connection.cursor()
        cursor.execute(query = 'some query')
        number_rows = 0
        rows = cursor.fetchall()
        for i in rows:
            number_rows += 1
        self.assertEqual(number_rows, 1)

    def test_fetch_with_one_row_returns_one_row_for_fetchone(self):
        mock_data = [
        [('field1', 'value1'), ('field2', 'value2')],
            ]
        connection = data_mock.psycopg2.connect( user='x', password='x', 
            host='x', port='x', database='x', mock_data = mock_data)
        cursor = connection.cursor()
        cursor.execute(query = 'some query')
        number_rows = 0
        rows = cursor.fetchone()
        for i in rows:
            number_rows += 1
        self.assertEqual(number_rows, 1)


if __name__ == '__main__':
    unittest.main()

