import boto3

from geowatchutil.buffer.base import GeoWatchBuffer
from geowatchutil.codec.factory import build_codec


class GeoWatchStore(object):

    # Public
    backend = None
    path = None

    # Private
    _buffer = None  # Used for temporarily caching messages locally before storing
    _codec = None

    def write_message(self, message, flush=False):
        self._buffer.add_message(message)
        if flush:
            self.flush()

    def write_messages(self, messages, flush=False):
        self._buffer.add_messages(messages)
        if flush:
            self.flush()

    def __init__(self, backend, path, codec):
        self.backend = backend
        self.path = path
        self._buffer = GeoWatchBuffer()
        self._codec = build_codec(codec)  # takes in well-known codec name and returns object


class GeoWatchStoreS3(GeoWatchStore):

    # Public
    bucket = None

    # Private
    _client = None

    def read(self):
        return self._codec.unpack(self._get())

    def _get(self):
        return self._client.get_object(Bucket=self.bucket, Key=self.path).decode('utf-8')

    def _put(self, package):
        return self._client.put_object(Bucket=self.bucket, Key=self.path, Body=package.encode('utf-8'))

    def flush(self):
        messages = self._buffer.get_messages()
        self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def __init__(self, path, codec, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, aws_bucket=None):
        super(GeoWatchStoreS3, self).__init__("s3", path, codec)

        if aws_region and aws_access_key_id and aws_secret_access_key and aws_bucket:
            session = boto3.session.Session(
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
            self._client = session.client('s3')
        else:
            print "Could not create GeoWatch client for S3 Backend.  Missing parameters."


class GeoWatchStoreMongoDB(GeoWatchStore):

    # Public
    bucket = None

    # Private
    _client = None

    def read(self):
        return self._codec.unpack(self._get())

    def _get(self):
        return self._client.get_object(Bucket=self.bucket, Key=self.path).decode('utf-8')

    def _put(self, package):
        return self._client.put_object(Bucket=self.bucket, Key=self.path, Body=package.encode('utf-8'))

    def flush(self):
        messages = self._buffer.get_messages()
        self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def __init__(self, path, codec, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, aws_bucket=None):
        super(GeoWatchStoreS3, self).__init__("s3", path, codec)

        if aws_region and aws_access_key_id and aws_secret_access_key and aws_bucket:
            session = boto3.session.Session(
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
            self._client = session.client('s3')
        else:
            print "Could not create GeoWatch client for S3 Backend.  Missing parameters."
