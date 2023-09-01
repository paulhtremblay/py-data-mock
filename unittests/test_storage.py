import hashlib
import base64
import sys
sys.path.append('.')
import unittest
from collections.abc import Iterable 

from data_mock.google.cloud import storage
CONTENT1= 'mock-contents'

class Mock1(storage.Client):

    def register_initial_mock_data(self):
        self.register_mock_data(blob_name = 'blob1', 
                bucket_name = 'mock-bucket', contents = CONTENT1 )

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

    def test_list_blobs_has_right_hash_and_right_number(self):
        storage_client = Mock1()
        blobs = storage_client.list_blobs(bucket_name = 'mock-bucket')
        local = hashlib.md5(CONTENT1.encode('utf8')).hexdigest()
        counter = 0
        for i in blobs:
            counter +=1
            v = base64.b64decode(i.md5_hash).hex()
            self.assertEqual(v, local)
        self.assertEqual(counter, 1)

if __name__ == '__main__':
    unittest.main()
