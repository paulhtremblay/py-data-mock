from data_mock.google.cloud.storage.bucket import Bucket

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
        pass

    def bucket(self, bucket_name, user_project=None):
        return Bucket(client=self, name=bucket_name, user_project=user_project)
