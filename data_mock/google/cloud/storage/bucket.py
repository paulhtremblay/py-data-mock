from data_mock.google.cloud.storage.blob import Blob

class Bucket():

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.client = kwargs['client']

    def blob(
        self,
        blob_name,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
    ):
        mock_blobs = self.client.mock_blobs
        for i in self.client.mock_blobs.get(self.name, []):
            if i.name == blob_name:
                return i

        return Blob(
            name=blob_name,
            bucket=self,
            chunk_size=chunk_size,
            encryption_key=encryption_key,
            kms_key_name=kms_key_name,
            generation=generation,
        )

    def list_blobs(self, prefix = None, *args, **kwargs):
        return self.client.list_blobs(bucket_or_name = self.name, prefix = prefix)
