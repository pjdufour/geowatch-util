from geowatchutil.producer.base import GeoWatchProducer

def build_producer(backend, topic, codec="plain", client=None, path=None, host=None, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, topic_prefix=""):
    producer = None
    if not client:
        if backend == "file" and path:
            client = create_client_file(path)
        if backend == "kafka" and host:
            client = create_client_kafka(host, topic_prefix)
        elif backend == "kinesis" and aws_region and aws_access_key_id and aws_secret_access_key:
            client = create_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix)
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            producer = GeoWatchProducerTileRequest(client, topic)
        else:
            producer = GeoWatchProducer(client, codec, topic)
    else:
        print "Could not create/use GeoWatch kinesis client!"
    return (client, producer)
