import boto3

from geowatchutil.buffer.base import GeoWatchBuffer
from geowatchutil.codec.factory import build_codec


class GeoWatchStore(object):

    # Public
    backend = None
    key = None  # or path

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

    def __init__(self, backend, key, codec):
        self.backend = backend
        self.key = key
        self._buffer = GeoWatchBuffer()
        self._codec = build_codec(codec)  # takes in well-known codec name and returns object


class GeoWatchStoreMemcached(GeoWatchStore):

    # Public
    bucket = None
    client_type = None

    # Private
    _client = None

    def read(self):
        return self._codec.unpack(self._get())

    def _get(self):
        if self.client_type == "umemcache":
            return None
        elif self.client_type == "pymemcache":
            return self._client.get(self.key)
        else:
            return None

    def _put(self, package):
        if self.client_type == "umemcache":
            return None
        elif self.client_type == "pymemcache":
            return self._client.set(self.key, package)
        else:
            return None

    def flush(self):
        messages = self._buffer.get_messages()
        self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def __init__(self, key, codec, cache_host=None, cache_port=None, cache_location=None, cache_params=None, client_type="pymemcache"):
        super(GeoWatchStoreMemcached, self).__init__("memcached", key, codec)
        self.client_type = client_type
        if cache_location and cache_params:
            if self.client_type == "umemcache":
                try:
                    # from umemcache import MemcachedError
                    from memcachepool.cache import UMemcacheCache
                    self._client = UMemcacheCache(cache_location, cache_params)
                except:
                    self._client = None
            elif self.client_tyoe == "pymemcache":
                try:
                    from pymemcache.client.base import Client
                    self._client = Client((cache_host, cache_port), default_noreply=False)  # Set default_noreply to not wait for response
                except:
                    self._client = None
        else:
            print "Could not create GeoWatch client for S3 Backend.  Missing parameters."


class GeoWatchStoreS3(GeoWatchStore):

    # Public
    bucket = None

    # Private
    _client = None

    def read(self):
        return self._codec.unpack(self._get())

    def _get(self):
        return self._client.get_object(Bucket=self.bucket, Key=self.key).decode('utf-8')

    def _put(self, package):
        return self._client.put_object(Bucket=self.bucket, Key=self.key, Body=package.encode('utf-8'))

    def flush(self):
        messages = self._buffer.get_messages()
        self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def create_bucket(self, bucket):
        return self._client.create_bucket(Bucket=self.bucket)

    def delete_bucket(self, bucket):
        return self._client.delete_bucket(Bucket=self.bucket)

    def __init__(self, key, codec, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, aws_bucket=None):
        super(GeoWatchStoreS3, self).__init__("s3", key, codec)

        if aws_region and aws_access_key_id and aws_secret_access_key and aws_bucket:
            session = boto3.session.Session(
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
            self._client = session.client('s3')
            self.bucket = aws_bucket
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
        return self._client.get_object(Bucket=self.bucket, Key=self.key).decode('utf-8')

    def _put(self, package):
        return self._client.put_object(Bucket=self.bucket, Key=self.key, Body=package.encode('utf-8'))

    def flush(self):
        messages = self._buffer.get_messages()
        self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def __init__(self, key, codec, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, aws_bucket=None):
        super(GeoWatchStoreS3, self).__init__("s3", key, codec)

        if aws_region and aws_access_key_id and aws_secret_access_key and aws_bucket:
            session = boto3.session.Session(
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
            self._client = session.client('s3')
        else:
            print "Could not create GeoWatch client for S3 Backend.  Missing parameters."
