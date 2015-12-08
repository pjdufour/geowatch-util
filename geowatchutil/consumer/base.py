import datetime

from geowatchutil.channel.factory import build_channel
from geowatchutil.node import GeoWatchNode


def assert_now(now):
    if not now:
        now = datetime.datetime.now()
    return now


class GeoWatchConsumer(GeoWatchNode):

    # Public
    num_procs = None

    # Private
    _channel = None

    def _get_messages_raw(self, count, block=True, timeout=5):
        return self._channel.get_messages_raw(count, block=block, timeout=timeout)

    def __init__(self, client, topic, codec, num_procs, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumer, self).__init__(client, topic, codec)
        self.num_procs = num_procs

        self._channel = build_channel(self._client.backend, topic=topic, mode="consumer", num_procs=num_procs, group=group, shard_id=shard_id, shard_it_type=shard_it_type)
