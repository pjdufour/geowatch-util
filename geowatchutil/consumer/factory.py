from geowatchutil.consumer.base import GeoWatchConsumer
from geowatchutil.consumer.geowatch_consumer_tilerequest import GeoWatchConsumerTileRequest


def build_consumer(client, codec, topic, **kwargs):
    consumer = None

    num_procs = kwargs.get('num_procs', 1)
    group = kwargs.get('group', None)
    shard_id = kwargs.get('shard_id', 'shardId-000000000000')
    shard_it_type = kwargs.get('shard_it_type', 'LATEST')

    codec_lc = codec.lower()
    if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
        consumer = GeoWatchConsumerTileRequest(
            client,
            topic,
            num_procs=num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
    else:
        consumer = GeoWatchConsumer(
            client,
            codec,
            topic,
            num_procs=num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
    return consumer

