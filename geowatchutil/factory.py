from geowatchutil.client.geowatch_client_files import GeoWatchClientFile
from geowatchutil.client.geowatch_client_kafka import GeoWatchClientKafka
from geowatchutil.client.geowatch_client_kinesis import GeoWatchClientKinesis
from geowatchutil.consumer.geowatch_consumer_plain import GeoWatchConsumerPlain
from geowatchutil.consumer.geowatch_consumer_json import GeoWatchConsumerJSON
from geowatchutil.consumer.geowatch_consumer_tilerequest import GeoWatchConsumerTileRequest
from geowatchutil.producer.geowatch_consumer_plain import GeoWatchProducerPlain
from geowatchutil.producer.geowatch_consumer_json import GeoWatchProducerJSON
from geowatchutil.producer.geowatch_consumer_tilerequest import GeoWatchProducerTileRequest


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


def create_consumer_file(codec="GeoWatchCodecPlain", path=None, client=None):
    consumer = None
    if path and not client:
        client = create_client_file(path)
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            consumer = GeoWatchConsumerTileRequest(client)
        elif codec_lc == "json" or codec_lc == "geowatchcodecjson":
            consumer = GeoWatchConsumerJSON(client)
        else:
            consumer = GeoWatchConsumerPlain(client)
    else:
        print "Could not create/use GeoWatch kafka client!"
    return (client, consumer)


def create_consumer_kafka(topic, codec="GeoWatchCodecPlain", num_procs=4, group='my-group', host=None, client=None, topic_prefix=""):
    consumer = None
    if host and not client:
        client = create_client_kafka(host, topic_prefix="")
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            consumer = GeoWatchConsumerTileRequest(client, topic, num_procs, group=group)
        elif codec_lc == "json" or codec_lc == "geowatchcodecjson":
            consumer = GeoWatchConsumerJSON(client, topic, num_procs, group=group)
        else:
            consumer = GeoWatchConsumerPlain(client, topic, num_procs, group=group)
    else:
        print "Could not create/use GeoWatch kafka client!"
    return (client, consumer)


def create_consumer_kinesis(topic, codec="GeoWatchCodecPlain", num_procs=1, client=None, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, shard_id='shardId-000000000000', shard_it_type="LATEST", topic_prefix=""):
    consumer = None
    if aws_region and aws_access_key_id and aws_secret_access_key and not client:
        client = create_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix)
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            consumer = GeoWatchConsumerTileRequest(client, topic, num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
        elif codec_lc == "json" or codec_lc == "geowatchcodecjson":
            consumer = GeoWatchConsumerJSON(client, topic, num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
        else:
            consumer = GeoWatchConsumerPlain(client, topic, num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
    else:
        print "Could not create/use GeoWatch kinesis client!"
    return (client, consumer)


def create_producer(backend, topic, codec="GeoWatchCodecPlain", client=None, path=None, host=None, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, topic_prefix=""):
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
        elif codec_lc == "json" or codec_lc == "geowatchcodecjson":
            producer = GeoWatchProducerJSON(client, topic)
        else:
            producer = GeoWatchProducerPlain(client, topic)
    else:
        print "Could not create/use GeoWatch kinesis client!"
    return (client, producer)
