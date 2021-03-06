from geowatchutil.channel.base import GeoWatchChannelTopic

from kafka import SimpleProducer, MultiProcessConsumer


class GeoWatchChannelKafka(GeoWatchChannelTopic):

    # Public
    group = None

    # Private
    _kafka_consumer = None
    _kafka_producer = None

    @classmethod
    def encode(cls, message):
        return message.encode('utf-8')

    @classmethod
    def decode(cls, message):
        return message.decode('utf-8')

    def send_message(self, message):
        self._kafka_producer.send_messages(self.topic, message)

    def send_messages(self, messages):
        self._kafka_producer.send_messages(self.topic, *messages)

    def get_messages_raw(self, count, block=True, timeout=5):
        return self._kafka_consumer.get_messages(count=count, block=True, timeout=timeout)

    def close(self):
        self._client.close()

    def __init__(self, client, topic, mode, num_procs=1, group=None):
        super(GeoWatchChannelKafka, self).__init__(client, topic, mode, num_procs=num_procs)
        self.group = group
        if mode == "duplex" or mode == "consumer":
            self._kafka_consumer = MultiProcessConsumer(self._client._client, self.group, self._client.topic_prefix + self.topic, num_procs=self.num_procs)
        if mode == "duplex" or mode == "producer":
            self._kafka_producer = SimpleProducer(self._client._client)
