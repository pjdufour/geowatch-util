from geowatch.store.geowatch_store_s3 import GeoWatchStoreS3


def build_store(backend, key, codec, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, aws_bucket=None):

    if backend == "s3":
        return GeoWatchStoreS3(
            key,
            codec,
            aws_region=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_bucket=aws_bucket)

