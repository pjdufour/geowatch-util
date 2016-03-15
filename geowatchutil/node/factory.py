from geowatchutil.base import GeoWatchError, GeoWatchModeError
from geowatchutil.node.base import GeoWatchNodeDuplex
from geowatchutil.node.geowatch_node_tilerequest import GeoWatchNodeTileRequest


def build_node(client, mode, codec, topic, **kwargs):

    if mode not in ["consumer", "producer", "duplex"]:
        raise GeoWatchModeError("GeoWatch mode error in build_node.")

    node = None
    codec_lc = codec.lower()
    buffer_outgoing = kwargs.pop('buffer_outgoing', None)

    if mode == "producer":
        if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
            node = GeoWatchNodeTileRequest(
                client,
                mode,
                topic,
                buffer_outgoing=buffer_outgoing)
        else:
            node = GeoWatchNodeDuplex(
                client,
                mode,
                codec,
                topic,
                buffer_outgoing=buffer_outgoing)
    elif mode == "consumer" or mode == "duplex":
        num_procs = kwargs.get('num_procs', 1)
        group = kwargs.get('group', None)
        it_id = kwargs.get('it_id', '0')
        it_type = kwargs.get('it_type', 'LATEST')
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
                shard_it_type=shard_it_type,
                buffer_outgoing=buffer_outgoing)
        else:
            node = GeoWatchNodeDuplex(
                client,
                mode,
                codec,
                topic,
                num_procs=num_procs,
                group=group,
                it_id=it_id,
                it_type=it_type,
                shard_id=shard_id,
                shard_it_type=shard_it_type,
                buffer_outgoing=buffer_outgoing)
    return node
