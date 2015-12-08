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

    def get_messages(self, count, block=True, timeout=5):
        response = self._get_messages_raw(count, block=block, timeout=timeout)
        if self._client.backend == "kafka":
            return self._receive_messages_plain_kafka(response)
        elif self._client.backend == "kinesis":
            return self._receive_messages_plain_kinesis(response)

    def _receive_messages_plain_kafka(self, response):
        messages = []
        for item in response:
            offset, message_raw = item
            messages.append(self._codec.decode(message_raw.value))
        return messages

    def _receive_messages_plain_kinesis(self, response):
        self._channel._shard_it = response[u'NextShardIterator']
        messages = []
        for item in response[u'Records']:
            # partition_key = item[u'PartitionKey']
            messages.append(self._codec.decode(item[u'Data']))
        return messages

    def _get_messages_raw(self, count, block=True, timeout=5):
        return self._channel.get_messages_raw(count, block=block, timeout=timeout)

    def __init__(self, client, codec, topic, num_procs=1, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumer, self).__init__(client, "consumer", codec, topic)
        self.num_procs = num_procs

        self._channel = build_channel(
            self._client.backend,
            topic=topic,
            mode="consumer",
            num_procs=num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
