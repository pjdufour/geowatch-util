import datetime

from geowatchutil.channel.factory import build_channel
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
        self._channel = build_channel(self._client.backend, topic=topic, mode="producer")
