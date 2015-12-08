import datetime

from geowatchutil.channel.factory import build_channel
from geowatchutil.node import GeoWatchNode


def assert_now(now):
    if not now:
        now = datetime.datetime.now()
    return now


class GeoWatchProducer(GeoWatchNode):

    def send_message(self, message):
        return self._channel.send_message(self._codec.encode(message))

    def send_messages(self, messages):
        messages_encoded = []
        for message in messages:
            messages_encoded.append(self._codec.encode(message))
        return self._channel.send_messages(messages_encoded)

    def __init__(self, client, codec, topic):
        super(GeoWatchProducer, self).__init__(client, "producer", codec, topic)
        self._channel = build_channel(self._client.backend, topic=topic, mode="producer")

