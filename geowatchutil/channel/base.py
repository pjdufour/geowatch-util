from geowatchutil.base import GeoWatchError


class GeoWatchChannel(object):

    # Public
    backend = None
    mode = None
    num_procs = None

    # Private
    _client = None

    def close(self):
        pass

    def __init__(self, client, mode, num_procs=1):
        self._client = client
        self.backend = self._client.backend
        self.mode = mode
        self.num_procs = num_procs

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()


class GeoWatchChannelTopic(GeoWatchChannel):

    # Public
    topic = None

    def __init__(self, client, topic, mode, num_procs=1):
        super(GeoWatchChannelTopic, self).__init__(client, mode, num_procs=1)
        self.topic = topic


class GeoWatchChannelError(GeoWatchError):

    def __init__(self, * args, ** kwargs):
        super(GeoWatchChannelError, self).__init__(self, * args, ** kwargs)
