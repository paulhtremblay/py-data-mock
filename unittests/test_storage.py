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

    def test_storage_can_create_client(self):
        storage_client = storage.Client(project = 'mock')
        bucket = storage_client.bucket(bucket_name = 'mock')
        blob = bucket.blob(blob_name = 'mock')

    def test_storage_upload_from_filename_succeeds(self):
        storage_client = storage.Client(project = 'mock')
        bucket = storage_client.bucket(bucket_name = 'mock')
        blob = bucket.blob(blob_name = 'mock')
        blob.upload_from_filename(filename = 'test')

if __name__ == '__main__':
    unittest.main()
