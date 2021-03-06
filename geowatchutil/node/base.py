"""
node/base.py includes the base GeoWatchNode class and the functional
GeoWatchNodeDuplex class.
"""
import datetime

from geowatchutil.codec.factory import build_codec
from geowatchutil.channel.factory import build_channel


def assert_now(now):
    if not now:
        now = datetime.datetime.now()
    return now


class GeoWatchNode(object):
    """
    GeoWatchNode is the base class for producers, consumers, and duplex nodes.

    """

    # Public
    topic = None
    """
        A string field that represents the topic.  In GeoWatch, ``topic`` represents an Apache Kafka topic, AWS Kinesis stream, AWS SNS topic, or any consumer/producer backend's topic.
    """

    mode = None
    """
        A string field that represents the mode.  Either: ``duplex``, ``consumer``, or ``producer``.
    """

    # Private
    _client = None
    _codec = None
    _channel = None

    def delete_topic(self, timeout=5, verbose=False):
        return self._client.delete_topic(self.topic, timeout=timeout, verbose=verbose)

    def __init__(self, client, mode, codec, topic):
        """
        """
        self._client = client
        self.mode = mode
        self.topic = topic

        # Codec
        self._codec = build_codec(codec, channel=self._client.backend, templates=self._client.templates)

        # Channel
        # Set by consumer/producer after GeoWatchNode.__init__
        self._channel = None


class GeoWatchNodeDuplex(GeoWatchNode):

    # Public
    num_procs = None

    # Consumer Functions
    def get_messages(self, count, block=True, timeout=5):
        response = self._get_messages_raw(count, block=block, timeout=timeout)
        if self._client.backend == "kafka":
            return self._receive_messages_plain_kafka(response)
        elif self._client.backend == "kinesis":
            return self._receive_messages_plain_kinesis(response)
        elif self._client.backend == "slack":
            return self._receive_messages_plain_slack(response)

    def _get_messages_raw(self, count, block=True, timeout=5):
        return self._channel.get_messages_raw(count, block=block, timeout=timeout)

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

    def _receive_messages_plain_slack(self, response):
        messages = []
        if response:
            for item in response:
                messages.append(self._codec.decode(item))
        print "messages", messages
        return messages

    # Producer Functions
    def send_message(self, message, **kwargs):
        if self._client.templates:
            return self._channel.send_message(self._codec.render(message), **kwargs)
        else:
            return self._channel.send_message(self._codec.encode(message, topic=self.topic), **kwargs)

    def send_messages(self, messages, **kwargs):
        messages_encoded = []
        for message in messages:
            if self._client.templates:
                messages_encoded.append(self._codec.render(message))
            else:
                messages_encoded.append(self._codec.encode(message, topic=self.topic))
        return self._channel.send_messages(messages_encoded, **kwargs)

    def close(self):
        self._channel.close()

    def __init__(self, client, mode, codec, topic, num_procs=1, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchNodeDuplex, self).__init__(client, mode, codec, topic)

        self._channel = build_channel(
            self._client.backend,
            client=self._client,
            topic=topic,
            mode=mode,
            num_procs=num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
