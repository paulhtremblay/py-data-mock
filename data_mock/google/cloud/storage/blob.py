from data_mock.mock_helpers import writer
import base64
import hashlib
import os



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
        mock_contents = None
        ):
        self.name = name
        self.mock_contents = mock_contents
        self._make_md5_hash(contents = mock_contents)
        self.bucket_name = bucket.name

    def _make_md5_hash(self, contents):
        if contents == None:
            return None
        hashed_v =  hashlib.md5(contents.encode('utf8')).digest()
        self.md5_hash =  base64.standard_b64encode(hashed_v)
         

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
                             verbosity = 0,
                             ):
        if not os.path.isfile(filename):
            if verbosity > 1:
                print('In mock storage: filename {filename} does not exist, so ignoring')
        else:
            with open(filename, 'r') as read_obj:
                self.mock_contents = ''.join(read_obj.readlines())
            self._make_md5_hash(contents = self.mock_contents)

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
        self.mock_contents = data
        self._make_md5_hash(contents = self.mock_contents)

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
        self.mock_contents = ''.join(file_obj.readlines())
        self._make_md5_hash(contents = self.mock_contents)

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
        if not self.mock_contents:
            pass #should raise 404
        return self.mock_contents.encode('utf8')

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
        if not self.mock_contents:
            pass #should raise 404
        return self.mock_contents.encode('utf8')

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
        if not self.mock_contents:
            pass #should raise 404
        return self.mock_contents

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
        if not self.mock_contents:
            pass #should raise 404
        file_obj.write(self.mock_contents)

    def download_to_filename(
        self,
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
        if not self.mock_contents:
            pass #should raise 404
        with open(filename, 'w') as write_obj:
            write_obj.write(self.mock_contents)

    def delete(self, *args, **kwargs):
        pass
