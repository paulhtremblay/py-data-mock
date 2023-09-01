import tempfile
import os
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

class Mock2(storage.Client):

    def register_initial_mock_data(self):
        self.register_mock_data(blob_name = 'dags/blob1', 
                bucket_name = 'mock-bucket', contents = CONTENT1 )
        self.register_mock_data(blob_name = 'dags/blob2', 
                bucket_name = 'mock-bucket', contents = CONTENT1 )
        self.register_mock_data(blob_name = 'other/blob2', 
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

    def test_storage_upload_from_filename_with_real_path_has_right_hash(self):
        fh, path = tempfile.mkstemp()
        with open(path, 'w') as write_obj:
            write_obj.write('mock-contents2')
        storage_client = storage.Client(project = 'mock')
        bucket = storage_client.bucket(bucket_name = 'mock')
        blob = bucket.blob(blob_name = 'mock')
        blob.upload_from_filename(filename = path)
        os.close(fh)
        os.remove(path)
        local_hash = hashlib.md5('mock-contents2'.encode('utf8')).hexdigest()
        blob_hash = base64.b64decode(blob.md5_hash).hex()
        self.assertEqual(blob_hash, local_hash)

    def test_storage_upload_from_string_has_right_hash(self):
        storage_client = storage.Client(project = 'mock')
        bucket = storage_client.bucket(bucket_name = 'mock')
        blob = bucket.blob(blob_name = 'mock')
        s = 'from-string1'
        blob.upload_from_string(data = s)
        local_hash = hashlib.md5(s.encode('utf8')).hexdigest()
        blob_hash = base64.b64decode(blob.md5_hash).hex()
        self.assertEqual(blob_hash, local_hash)

    def test_storage_upload_from_file_has_right_hash(self):
        data = 'from-file1'
        fh, path = tempfile.mkstemp()
        with open(path, 'w') as write_obj:
            write_obj.write(data)
        file_obj = open(path, 'r')
        storage_client = storage.Client(project = 'mock')
        bucket = storage_client.bucket(bucket_name = 'mock')
        blob = bucket.blob(blob_name = 'mock')
        blob.upload_from_file(file_obj = file_obj)
        local_hash = hashlib.md5(data.encode('utf8')).hexdigest()
        blob_hash = base64.b64decode(blob.md5_hash).hex()
        self.assertEqual(blob_hash, local_hash)

    def test_download_as_bytes(self):
        storage_client = Mock1()
        bucket = storage_client.bucket(bucket_name = 'mock-bucket')
        blob = bucket.blob('blob1')
        r = blob.download_as_bytes()
        self.assertEqual(r, CONTENT1.encode('utf8'))

    def test_download_as_string(self):
        storage_client = Mock1()
        bucket = storage_client.bucket(bucket_name = 'mock-bucket')
        blob = bucket.blob('blob1')
        r = blob.download_as_string()
        self.assertEqual(r, CONTENT1.encode('utf8'))

    def test_download_as_text(self):
        storage_client = Mock1()
        bucket = storage_client.bucket(bucket_name = 'mock-bucket')
        blob = bucket.blob('blob1')
        r = blob.download_as_text()
        self.assertEqual(r, CONTENT1)

    def test_download_to_file(self):
        fh, path = tempfile.mkstemp()
        file_obj = open(path, 'w')
        storage_client = Mock1()
        bucket = storage_client.bucket(bucket_name = 'mock-bucket')
        blob = bucket.blob('blob1')
        blob.download_to_file(file_obj = file_obj)
        file_obj.close()
        with open(path, 'r') as read_obj:
            r = ''.join(read_obj.readlines())
        self.assertEqual(r, CONTENT1)
        os.close(fh)
        os.remove(path)

    def test_download_to_filename(self):
        fh, path = tempfile.mkstemp()
        storage_client = Mock1()
        bucket = storage_client.bucket(bucket_name = 'mock-bucket')
        blob = bucket.blob('blob1')
        blob.download_to_filename(filename = path)
        with open(path, 'r') as read_obj:
            r = ''.join(read_obj.readlines())
        self.assertEqual(r, CONTENT1)
        os.close(fh)
        os.remove(path)


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
        blobs = storage_client.list_blobs(bucket_or_name = 'mock-bucket')
        local = hashlib.md5(CONTENT1.encode('utf8')).hexdigest()
        counter = 0
        for i in blobs:
            counter +=1
            v = base64.b64decode(i.md5_hash).hex()
            self.assertEqual(v, local)
        self.assertEqual(counter, 1)

    def test_list_blobs_no_result_diff_bucket(self):
        storage_client = Mock1()
        blobs = storage_client.list_blobs(bucket_or_name = 'mock-bucket-not-exist')
        local = hashlib.md5(CONTENT1.encode('utf8')).hexdigest()
        counter = 0
        for i in blobs:
            counter +=1
        self.assertEqual(counter, 0)

    def test_list_blobs_with_prefix_not_sure(self):
        storage_client = Mock2()
        blobs = storage_client.list_blobs(bucket_or_name = 'mock-bucket',
                                          prefix = 'dags/')
        local = hashlib.md5(CONTENT1.encode('utf8')).hexdigest()
        counter = 0
        for i in blobs:
            counter +=1
        self.assertEqual(counter, 2)

    def test_list_blobs_with_bucket_has_right_hash_and_right_number(self):
        storage_client = Mock1()
        bucket = storage_client.bucket(bucket_name = 'mock-bucket')
        blobs = bucket.list_blobs()
        local = hashlib.md5(CONTENT1.encode('utf8')).hexdigest()
        counter = 0
        for i in blobs:
            counter +=1
            v = base64.b64decode(i.md5_hash).hex()
            self.assertEqual(v, local)
        self.assertEqual(counter, 1)


if __name__ == '__main__':
    unittest.main()
