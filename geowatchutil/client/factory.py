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


def build_client_sns(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix, templates):
    from geowatchutil.client.geowatch_client_sns import GeoWatchClientSNS
    return GeoWatchClientSNS(
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        topic_prefix=topic_prefix,
        templates=templates)


def build_client_slack(url_webhook, authtoken, templates):
    from geowatchutil.client.geowatch_client_slack import GeoWatchClientSlack
    return GeoWatchClientSlack(url_webhook=url_webhook, authtoken=authtoken, templates=templates)


def build_client_wfs(url_wfs, auth_user, auth_password):
    from geowatchutil.client.geowatch_client_wfs import GeoWatchClientWFS
    return GeoWatchClientWFS(
        url_wfs=url_wfs,
        auth_user=auth_user,
        auth_password=auth_password)


def build_client(backend, **kwargs):
    """
    build_client returns a GeoWatchClient.  build_client is used by runtime.py.  For individual use cases, directly calling the subordinate functions such as build_client_kafka might make sense.
    """
    client = None
    if backend == "file":
        client = build_client_file(kwargs.get('path', None))
    elif backend == "kafka":
        client = build_client_kafka(kwargs.get('host', None), kwargs.get('topic_prefix', None))
    elif backend == "kinesis":
        client = build_client_kinesis(
            kwargs.get('aws_region', None),
            kwargs.get('aws_access_key_id', None),
            kwargs.get('aws_secret_access_key'),
            kwargs.get('topic_prefix'))
    elif backend == "wfs":
        client = build_client_wfs(kwargs.get('url', None), kwargs.get('auth_user', None), kwargs.get('auth_password', None))
    elif backend == "sns":
        client = build_client_sns(
            kwargs.get('aws_region', None),
            kwargs.get('aws_access_key_id', None),
            kwargs.get('aws_secret_access_key', None),
            kwargs.get('topic_prefix', None),
            kwargs.get('templates', None))
    elif backend == "slack":
        client = build_client_slack(kwargs.get('url_webhook', None), kwargs.get('authtoken', None), kwargs.get('templates', None))
    return client
