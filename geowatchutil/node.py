
class GeoWatchNode(object):

    # Public
    topic = None

    # Private
    _client = None
    _codec = None

    def __init__(self, client, topic, codec):
        self._client = client
        self.topic = topic
        self._codec = codec
        self._codec.setChannel(self._client.backend)
