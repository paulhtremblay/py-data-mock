import sys

from collections.abc import Iterable
from collections import OrderedDict

sys.path.append('.')
import unittest

import data_mock.psycopg3 as psycopg

class TestPsycopg3(unittest.TestCase):

    def test_basic_functionality(self):
        with psycopg.connect("dbname=test user=postgres") as conn:
            with conn.cursor() as cur:
                cur.execute(query = '')
                r = cur.fetchone()
                for i in r:
                    pass
                conn.commit()
                conn.rollback()
                for i in cur:
                    pass

if __name__ == '__main__':
    unittest.main()
