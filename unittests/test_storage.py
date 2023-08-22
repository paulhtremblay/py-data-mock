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

    def test_get_bucket_has_blob_attribute(self):
        storage_client = storage.Client(project = 'mock')
        o = storage_client.get_bucket(bucket_name = 'mock')
        self.assertTrue(hasattr(o, 'blob'))

    def test_blob_has_delete(self):
        storage_client = storage.Client(project = 'mock')
        bucket = storage_client.bucket(bucket_name = 'mock')
        blob = bucket.blob(blob_name = 'mock')
        blob.delete()

if __name__ == '__main__':
    unittest.main()
