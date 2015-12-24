import datetime

from geowatchutil.channel.factory import build_channel
from geowatchutil.node import GeoWatchNode


def assert_now(now):
    if not now:
        now = datetime.datetime.now()
    return now


class GeoWatchProducer(GeoWatchNode):

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

    def __init__(self, client, codec, topic):
        super(GeoWatchProducer, self).__init__(client, "producer", codec, topic)
        self._channel = build_channel(
            self._client.backend,
            client=self._client,
            topic=topic,
            mode="producer")

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
