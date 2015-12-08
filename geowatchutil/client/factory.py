from geowatchutil.client.geowatch_client_files import GeoWatchClientFile
from geowatchutil.client.geowatch_client_kafka import GeoWatchClientKafka
from geowatchutil.client.geowatch_client_kinesis import GeoWatchClientKinesis
from geowatchutil.client.geowatch_client_slack import GeoWatchClientSlack


def build_client_file(path):
    return GeoWatchClientFile(path=path)


def build_client_kafka(host, topic_prefix):
    return GeoWatchClientKafka(host=host, topic_prefix=topic_prefix)


def build_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix):
    return GeoWatchClientKinesis(
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        topic_prefix=topic_prefix)


def build_client_slack(url_webhook, authtoken):
    return GeoWatchClientSlack(url_webhook=url_webhook, authtoken=authtoken)
