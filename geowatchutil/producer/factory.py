from geowatchutil.producer.factory import build_client_file, build_client_kafka, build_client_kinesis, build_client_slack
from geowatchutil.producer.base import GeoWatchProducer
from geowatchutil.producer.geowatch_producer_tilerequest import GeoWatchProducerTileRequest


def build_producer(backend, topic, codec="plain", client=None, path=None, host=None, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, topic_prefix="", url_webhook="", authtoken=""):
    producer = None
    if not client:
        if backend == "file" and path:
            client = build_client_file(path)
        if backend == "kafka" and host:
            client = build_client_kafka(host, topic_prefix)
        elif backend == "kinesis" and aws_region and aws_access_key_id and aws_secret_access_key:
            client = build_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix)
        elif backend == "slack" and (url_webhook or authtoken):
            client = build_client_slack(url_webhook, authtoken)
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            producer = GeoWatchProducerTileRequest(client, topic)
        else:
            producer = GeoWatchProducer(client, codec, topic)
    else:
        print "Could not create/use GeoWatch kinesis client!"
    return (client, producer)
