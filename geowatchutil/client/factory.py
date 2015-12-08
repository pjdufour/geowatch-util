from geowatchutil.client.geowatch_client_files import GeoWatchClientFile
from geowatchutil.client.geowatch_client_kafka import GeoWatchClientKafka
from geowatchutil.client.geowatch_client_kinesis import GeoWatchClientKinesis


def create_client_file(path):
    return GeoWatchClientFile(path=path)


def create_client_kafka(host, topic_prefix):
    return GeoWatchClientKafka(host=host, topic_prefix=topic_prefix)


def create_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix):
    return GeoWatchClientKinesis(
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        topic_prefix=topic_prefix)
