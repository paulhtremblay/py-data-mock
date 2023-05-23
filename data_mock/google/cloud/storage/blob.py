from data_mock.mock_helpers import writer
class Blob:

    _DEFAULT_TIMEOUT = 1
    _DEFAULT_RETRY_IF_GENERATION_SPECIFIED = None
    DEFAULT_RETRY_IF_GENERATION_SPECIFIED = None

    def __init__(self,
        name,
        bucket,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
        ):
        pass

    def upload_from_filename(self):
        pass

    def upload_from_string(self,
        data,
        content_type="text/plain",
        num_retries=None,
        client=None,
        predefined_acl=None,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        timeout=_DEFAULT_TIMEOUT,
        checksum=None,
        retry=DEFAULT_RETRY_IF_GENERATION_SPECIFIED,
        write_class = writer.Writer(),
        ):
        write_class.write_to_storage_from_string(data = data)

    def upload_from_file(self):
        pass

    def download_as_bytes(self):
        pass

    def download_as_string(self):
        pass

    def download_as_text(self):
        pass

    def download_to_file(self):
        pass
    def download_to_filename(self):
        pass
