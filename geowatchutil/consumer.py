import datetime

from geowatchutil.base import parse_date, is_expired
from geowatchutil.channel import GeoWatchChannelFile, GeoWatchChannelKafka, GeoWatchChannelKinesis
from geowatchutil.codec import GeoWatchCodecPlain, GeoWatchCodecJSON, GeoWatchCodecTileRequest
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

    def get_messages_raw(self, count, block=True, timeout=5):
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


class GeoWatchConsumerPlain(GeoWatchConsumer):

    def receive_messages_plain(self, count, block=True, timeout=5):
        response = self.get_messages_raw(count, block=block, timeout=timeout)
        if self._client.backend == "kafka":
            return self._receive_messages_plain_kafka(response)
        elif self._client.backend == "kinesis":
            return self._receive_messages_plain_kinesis(response)

    def _receive_messages_plain_kafka(self, response):
        messages = []
        for item in response:
            offset, message_raw = item
            messages.append(self._codec.decode_channel(message_raw.value))
        return messages

    def _receive_messages_plain_kinesis(self, response):
        self._channel._shard_it = response[u'NextShardIterator']
        messages = []
        for item in response[u'Records']:
            # partition_key = item[u'PartitionKey']
            messages.append(self._codec.decode_channel(item[u'Data']))
        return messages

    def __init__(self, client, topic, num_procs, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumerPlain, self).__init__(
            client,
            topic,
            GeoWatchCodecPlain(channel=client.backend),
            num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)


class GeoWatchConsumerJSON(GeoWatchConsumer):

    def __init__(self, client, topic, num_procs, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumerJSON, self).__init__(
            client,
            topic,
            GeoWatchCodecJSON(channel=client.backend),
            num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)


class GeoWatchConsumerTileRequest(GeoWatchConsumer):

    def receive_tile_requests(self, count, ttl=60, block=True, timeout=5, now=None):
        now = assert_now(now)
        response = self.get_messages_raw(count, block=block, timeout=timeout)
        if self._client.backend == "kafka":
            return self._receive_tile_requests_kafka(response, now, ttl)
        elif self._client.backend == "kinesis":
            return self._receive_tile_requests_kinesis(response, now, ttl)

    def _receive_tile_requests_kafka(self, response, now, ttl):
        messages_decoded = []
        for item in response:
            offset, message = item
            message_decoded = self._codec.decode_channel(message.value)
            itempart = message_decoded.split(";")
            date = parse_date(itempart[0])
            if not date:
                print "Date is missing or invalid!"
            elif is_expired(date, now, ttl):
                # print "Tile expired!"
                continue
            else:
                messages_decoded.append(itempart[1])  # Covert to dict within client application

        return messages_decoded

    def _receive_tile_requests_kinesis(self, response, now, ttl):
        self._channel._shard_it = response[u'NextShardIterator']
        messages_decoded = []
        for item in response[u'Records']:
            # partition_key = item[u'PartitionKey']
            message = item[u'Data']
            message_decoded = self._codec.decode_channel(message)
            itempart = message_decoded.split(";")
            date = parse_date(itempart[0])
            if not date:
                print "Date is missing or invalid!"
            elif is_expired(date, now, ttl):
                # print "Tile expired!"
                continue
            else:
                messages_decoded.append(itempart[1])  # Covert to dict within client application

        return messages_decoded

    def __init__(self, client, topic, num_procs, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumerTileRequest, self).__init__(
            client,
            topic,
            GeoWatchCodecTileRequest(channel=client.backend),
            num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
