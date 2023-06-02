import sys
sys.path.append('.')
from decimal import Decimal
import time
import datetime
from datetime import timezone
#import pytz


import unittest
from data_mock.google.cloud.bigquery import SchemaField
from data_mock.mock_helpers import generate_data

class TestMakeMockData(unittest.TestCase):

    def test_generate_STRING_is_str(self):
        c = generate_data.MakeMockBQData()
        s = c.make_STRING(name = 'foo')
        self.assertTrue(isinstance(s, str))

    def test_generate_BYTES_is_bytes(self):
        c = generate_data.MakeMockBQData()
        s = c.make_BYTES(name = 'foo')
        self.assertTrue(isinstance(s, bytes))

    def test_generate_INT64_is_int(self):
        c = generate_data.MakeMockBQData()
        i = c.make_INT64(name = 'foo')
        self.assertTrue(isinstance(i, int))

    def test_generate_FLOAT_is_float(self):
        c = generate_data.MakeMockBQData()
        i = c.make_FLOAT(name = 'foo')
        self.assertTrue(isinstance(i, float))

    def test_generate_FLOAT64_is_float(self):
        c = generate_data.MakeMockBQData()
        i = c.make_FLOAT64(name = 'foo')
        self.assertTrue(isinstance(i, float))

    def test_generate_NUMERIC_is_decimal(self):
        c = generate_data.MakeMockBQData()
        i = c.make_NUMERIC(name = 'foo')
        self.assertTrue(isinstance(i, Decimal))

    def test_generate_BOOLEAN_is_boolean(self):
        c = generate_data.MakeMockBQData()
        i = c.make_BOOLEAN(name = 'foo')
        self.assertTrue(isinstance(i, bool))

    def test_generate_BOOL_is_boolean(self):
        c = generate_data.MakeMockBQData()
        i = c.make_BOOL(name = 'foo')
        self.assertTrue(isinstance(i, bool))

    def test_generate_TIMESTAMP_is_datetime_with_tz_info(self):
        c = generate_data.MakeMockBQData()
        t = c.make_TIMESTAMP(name = 'foo')
        self.assertTrue(isinstance(t, datetime.datetime))
        self.assertTrue(t.tzinfo != None)

    def test_generate_DATE_is_date(self):
        c = generate_data.MakeMockBQData()
        t = c.make_DATE(name = 'foo')
        self.assertTrue(isinstance(t, datetime.date))

    def test_generate_DATETIME_is_date(self):
        c = generate_data.MakeMockBQData()
        t = c.make_DATETIME(name = 'foo')
        self.assertTrue(isinstance(t, datetime.datetime))

    def test_generate_TIME_is_time(self):
        c = generate_data.MakeMockBQData()
        t = c.make_TIME(name = 'foo')
        self.assertTrue(isinstance(t, datetime.time))

if __name__ == '__main__':
    unittest.main()
