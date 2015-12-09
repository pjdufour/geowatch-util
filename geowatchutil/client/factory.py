def build_client_file(path):
    from geowatchutil.client.geowatch_client_files import GeoWatchClientFile
    return GeoWatchClientFile(path=path)


def build_client_kafka(host, topic_prefix):
    from geowatchutil.client.geowatch_client_kafka import GeoWatchClientKafka
    return GeoWatchClientKafka(host=host, topic_prefix=topic_prefix)


def build_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix):
    from geowatchutil.client.geowatch_client_kinesis import GeoWatchClientKinesis
    return GeoWatchClientKinesis(
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        topic_prefix=topic_prefix)


def build_client_slack(url_webhook, authtoken, templates):
    from geowatchutil.client.geowatch_client_slack import GeoWatchClientSlack
    return GeoWatchClientSlack(url_webhook=url_webhook, authtoken=authtoken, templates=templates)
