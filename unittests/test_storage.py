import sys
sys.path.append('.')
import unittest
from collections.abc import Iterable 

from data_mock.google.cloud import storage

class TestStorage(unittest.TestCase):

    def setUp(self):
        pass

    def  tearDown(self):
        pass

    def test_storage_unsure(self):
        storage_client = storage.Client(project = 'paulhenrytremblay')
        bucket = storage_client.bucket(bucket_name = 'mock')
        blob = bucket.blob(blob_name = 'mock')

if __name__ == '__main__':
    unittest.main()
