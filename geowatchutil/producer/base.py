import datetime

from geowatchutil.channel import GeoWatchChannelFile, GeoWatchChannelKafka, GeoWatchChannelKinesis
from geowatchutil.codec import GeoWatchCodecPlain, GeoWatchCodecJSON, GeoWatchCodecTileRequest
from geowatchutil.node import GeoWatchNode


def assert_now(now):
    if not now:
        now = datetime.datetime.now()
    return now


class GeoWatchProducer(GeoWatchNode):
    _channel = None

    def send_message(self, message):
        self._channel.send_message(message)

    def send_messages(self, messages):
        self._channel.send_messages(messages)

    def __init__(self, client, topic, codec):
        super(GeoWatchProducer, self).__init__(client, topic, codec)

        if self._client.backend == "file":
            self._channel = GeoWatchChannelFile(client, "producer")
        elif self._client.backend == "kafka":
            self._channel = GeoWatchChannelKafka(client, topic, "producer")
        elif self._client.backend == "kinesis":
            self._channel = GeoWatchChannelKinesis(client, topic, "producer")
        elif self._client.backend == "sns":
            self._channel = GeoWatchChannelSNS(client, topic, "producer")
