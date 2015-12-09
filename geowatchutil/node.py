from geowatchutil.codec.factory import build_codec


class GeoWatchNode(object):

    # Public
    topic = None
    mode = None

    # Private
    _client = None
    _codec = None
    _channel = None

    def __init__(self, client, mode, codec, topic):
        self._client = client
        self.mode = mode
        self.topic = topic

        # Codec
        self._codec = build_codec(codec, channel=self._client.backend, templates=self._client.templates)

        # Channel
        # Set by consumer/producer after GeoWatchNode.__init__
        self._channel = None
