from geowatchutil.client.factory import create_client_file, create_client_kafka, create_client_kinesis
from geowatchutil.consumer.base import GeoWatchConsumer
from geowatchutil.consumer.geowatch_consumer_tilerequest import GeoWatchConsumerTileRequest


def create_consumer_file(codec="plain", path=None, client=None):
    consumer = None
    if path and not client:
        client = create_client_file(path)
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            consumer = GeoWatchConsumerTileRequest(client, "")
        else:
            consumer = GeoWatchConsumer(client, codec, "")
    else:
        print "Could not create/use GeoWatch kafka client!"
    return (client, consumer)


def create_consumer_kafka(topic, codec="plain", num_procs=4, group='my-group', host=None, client=None, topic_prefix=""):
    consumer = None
    if host and not client:
        client = create_client_kafka(host, topic_prefix="")
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            consumer = GeoWatchConsumerTileRequest(client, topic, num_procs=num_procs, group=group)
        else:
            consumer = GeoWatchConsumer(client, codec, topic, num_procs=num_procs, group=group)
    else:
        print "Could not create/use GeoWatch kafka client!"
    return (client, consumer)


def create_consumer_kinesis(topic, codec="plain", num_procs=1, client=None, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, shard_id='shardId-000000000000', shard_it_type="LATEST", topic_prefix=""):
    consumer = None
    if aws_region and aws_access_key_id and aws_secret_access_key and not client:
        client = create_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix)
    if client:
        codec_lc = codec.lower()
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            consumer = GeoWatchConsumerTileRequest(client, topic, num_procs=num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
        else:
            consumer = GeoWatchConsumer(client, codec, topic, num_procs=num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
    else:
        print "Could not create/use GeoWatch kinesis client!"
    return (client, consumer)
