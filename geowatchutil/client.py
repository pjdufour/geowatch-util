class GeoWatchClient(object):

    # Public
    backend = None

    # Private
    _client = None

    def __init__(self, backend=""):
        self._client = None
        self.backend = backend


class GeoWatchClientTopic(GeoWatchClient):

    # Public
    topic_prefix = ""

    def __init__(self, backend="", topic_prefix=""):
        super(GeoWatchClientTopic, self).__init__(backend=backend)
        self.topic_prefix = topic_prefix
