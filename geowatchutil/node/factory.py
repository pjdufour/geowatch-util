from geowatchutil.node.base import GeoWatchNodeDuplex
from geowatchutil.node.geowatch_node_tilerequest import GeoWatchNodeTileRequest


def build_node(client, mode, codec, topic, **kwargs):
    node = None
    codec_lc = codec.lower()
    if mode == "producer":
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            node = GeoWatchNodeTileRequest(client, mode, topic)
        else:
            node = GeoWatchNodeDuplex(client, mode, codec, topic)
    elif mode == "consumer" or mode == "duplex":
        num_procs = kwargs.get('num_procs', 1)
        group = kwargs.get('group', None)
        shard_id = kwargs.get('shard_id', 'shardId-000000000000')
        shard_it_type = kwargs.get('shard_it_type', 'LATEST')
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            node = GeoWatchNodeTileRequest(
                client,
                mode,
                topic,
                num_procs=num_procs,
                group=group,
                shard_id=shard_id,
                shard_it_type=shard_it_type)
        else:
            node = GeoWatchNodeDuplex(
                client,
                mode,
                codec,
                topic,
                num_procs=num_procs,
                group=group,
                shard_id=shard_id,
                shard_it_type=shard_it_type)
    return node
