from kafka import SimpleProducer, MultiProcessConsumer


class GeoWatchChannel(object):

    # Public
    backend = None
    mode = None
    num_procs = None

    # Private
    _client = None

    def __init__(self, client, mode, num_procs=1):
        self._client = client
        self.backend = self._client.backend
        self.mode = mode
        self.num_procs = num_procs


class GeoWatchChannelTopic(GeoWatchChannel):

    # Public
    topic = None

    def __init__(self, client, topic, mode, num_procs=1):
        super(GeoWatchChannelTopic, self).__init__(client, mode, num_procs=1)
        self.topic = topic
