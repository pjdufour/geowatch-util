import datetime

from geowatchutil.channel.geowatch_channel_file import GeoWatchChannelFile
from geowatchutil.channel.geowatch_channel_kafka import GeoWatchChannelKafka
from geowatchutil.channel.geowatch_channel_kinesis import GeoWatchChannelKinesis
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

        if self._client.backend == "file":
            self._channel = GeoWatchChannelFile(client, "consumer")
        if self._client.backend == "kafka":
            self._channel = GeoWatchChannelKafka(client, topic, "consumer", num_procs=num_procs, group=group)
        elif self._client.backend == "kinesis":
            self._channel = GeoWatchChannelKinesis(client, topic, "consumer", num_procs=num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
