from data_mock.mock_helpers import writer
class Blob:

    _DEFAULT_TIMEOUT = 1
    _DEFAULT_RETRY_IF_GENERATION_SPECIFIED = None
    DEFAULT_RETRY_IF_GENERATION_SPECIFIED = None
    DEFAULT_RETRY = 1

    def __init__(self,
        name,
        bucket,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
        ):
        self.name = name

    def upload_from_filename(self, 
                             filename,
                            content_type=None,
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
                             ):
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

    def upload_from_file(self,
        file_obj,
        rewind=False,
        size=None,
        content_type=None,
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
                         ):
        pass

    def download_as_bytes(
        self,
        client=None,
        start=None,
        end=None,
        raw_download=False,
        if_etag_match=None,
        if_etag_not_match=None,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        timeout=_DEFAULT_TIMEOUT,
        checksum="md5",
        retry=DEFAULT_RETRY,
        ):
        pass

    def download_as_string(
        self,
        client=None,
        start=None,
        end=None,
        raw_download=False,
        if_etag_match=None,
        if_etag_not_match=None,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        timeout=_DEFAULT_TIMEOUT,
        retry=DEFAULT_RETRY,
        ):
        pass

    def download_as_text(
        self,
        client=None,
        start=None,
        end=None,
        raw_download=False,
        encoding=None,
        if_etag_match=None,
        if_etag_not_match=None,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        timeout=_DEFAULT_TIMEOUT,
        retry=DEFAULT_RETRY,
        ):
        pass

    def download_to_file(
        self,
        file_obj,
        client=None,
        start=None,
        end=None,
        raw_download=False,
        if_etag_match=None,
        if_etag_not_match=None,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        timeout=_DEFAULT_TIMEOUT,
        checksum="md5",
        retry=DEFAULT_RETRY,
        ):
        pass

    def download_to_filename(
        filename,
        client=None,
        start=None,
        end=None,
        raw_download=False,
        if_etag_match=None,
        if_etag_not_match=None,
        if_generation_match=None,
        if_generation_not_match=None,
        if_metageneration_match=None,
        if_metageneration_not_match=None,
        timeout=_DEFAULT_TIMEOUT,
        checksum="md5",
        retry=DEFAULT_RETRY,
        ):
        pass
