from data_mock.google.cloud.storage.bucket import Bucket
from data_mock.google.cloud.storage.blob import Blob

class Client:
    _marker = None

    def __init__(self,
        project=_marker,
        credentials=None,
        _http=None,
        client_info=None,
        client_options=None,
        use_auth_w_custom_endpoint=True,
            ):
        self.mock_blobs = {}
        self.register_initial_mock_data()

    def register_initial_mock_data(self):
        pass

    def register_mock_data(self, blob_name, bucket_name, contents ):
        blob = Blob(name = blob_name, mock_contents = contents, bucket = self.bucket(bucket_name = bucket_name))
        if not self.mock_blobs.get(bucket_name):
            self.mock_blobs[bucket_name] = []
        self.mock_blobs[bucket_name].append(blob)

    def _mock_create_blobs(self):
        pass

    def bucket(self, bucket_name, user_project=None):
        return Bucket(client=self, name=bucket_name, user_project=user_project)

    def get_bucket(self,
                   bucket_name,
                   user_project = None):
        return Bucket(client=self, name=bucket_name, user_project=user_project)


    def _mock_gen_func(self, bucket_name, prefix):
        l = self.mock_blobs.get(bucket_name, [])
        for i in l:
            if prefix and  not i.name.startswith(prefix):
                continue
            yield i

    def list_blobs(self, bucket_or_name, prefix = None, *args, **kwargs):
        if hasattr(bucket_or_name, 'name'):
            name = bucket_or_name.name
        else:
            name = bucket_or_name
        return self._mock_gen_func(
                bucket_name = name,
                prefix = prefix)
