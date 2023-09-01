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
        self.mock_blobs = []
        self.register_initial_mock_data()

    def register_initial_mock_data(self):
        pass

    def register_mock_data(self, name, contents = None):
        bucket = self.bucket('bucket_name')
        blob = Blob(name = name, mock_contents = contents, bucket = self.bucket)
        self.mock_blobs.append(blob)

    def _mock_create_blobs(self):
        pass


    def bucket(self, bucket_name, user_project=None):
        return Bucket(client=self, name=bucket_name, user_project=user_project)

    def get_bucket(self,
                   bucket_name,
                   user_project = None):
        return Bucket(client=self, name=bucket_name, user_project=user_project)

    def list_blobs(self, bucket_name, *args, **kwargs):
        return self.mock_blobs
