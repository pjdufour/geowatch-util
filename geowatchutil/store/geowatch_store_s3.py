import boto3

from geowatchutil.store.base import GeoWatchStore


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
        return self._client.put_object(
            Bucket=self.bucket,
            Key=self.key,
            Body=package.encode('utf-8'),
            ContentType=self._codec.content_type)

    def flush(self):
        messages = self._buffer.get_messages()
        if self.which == "first":
            self._put(self._codec.pack(messages, which=self.which))  # _codec.pack returns text representation
        elif self.which == "index":
            self._put(self._codec.pack(messages, which=self.which, which_index=self.which_index))  # _codec.pack returns text representation
        else:
            self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def create_bucket(self, bucket):
        return self._client.create_bucket(Bucket=self.bucket)

    def delete_bucket(self, bucket):
        return self._client.delete_bucket(Bucket=self.bucket)

    def __init__(self, key, codec, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, aws_bucket=None, which="all", which_index=0):
        super(GeoWatchStoreS3, self).__init__("s3", key, codec, which=which, which_index=which_index)

        if aws_region and aws_access_key_id and aws_secret_access_key and aws_bucket:
            session = boto3.session.Session(
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
            self._client = session.client('s3')
            self.bucket = aws_bucket
        else:
            print "Could not create GeoWatch client for S3 Backend.  Missing parameters."
