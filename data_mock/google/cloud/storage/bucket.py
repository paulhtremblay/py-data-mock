from data_mock.google.cloud.storage.blob import Blob

class Bucket():

    def __init__(self, *args, **kwargs):
        pass

    def blob(
        self,
        blob_name,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
    ):
        return Blob(
            name=blob_name,
            bucket=self,
            chunk_size=chunk_size,
            encryption_key=encryption_key,
            kms_key_name=kms_key_name,
            generation=generation,
        )
