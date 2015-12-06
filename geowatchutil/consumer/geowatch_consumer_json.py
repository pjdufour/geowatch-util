from geowatchutil.consumer.base import GeoWatchConsumer

from geowatchutil.codec.geowatch_codec_json import GeoWatchCodecJSON


class GeoWatchConsumerJSON(GeoWatchConsumer):

    def get_messages(self, count, block=True, timeout=5):
        response = self.get_messages_raw(count, block=block, timeout=timeout)
        if self._client.backend == "kafka":
            return self._receive_messages_json_kafka(response)
        elif self._client.backend == "kinesis":
            return self._receive_messages_json_kinesis(response)

    def _receive_messages_json_kafka(self, response):
        messages = []
        for item in response:
            offset, message_raw = item
            messages.append(self._codec.decode(data=message_raw.value))
        return messages

    def _receive_messages_json_kinesis(self, response):
        self._channel._shard_it = response[u'NextShardIterator']
        messages = []
        for item in response[u'Records']:
            # partition_key = item[u'PartitionKey']
            messages.append(self._codec.decode(data=item[u'Data']))
        return messages

    def __init__(self, client, topic, num_procs, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumerJSON, self).__init__(
            client,
            topic,
            GeoWatchCodecJSON(channel=client.backend),
            num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
