from geowatchutil.channel.base import GeoWatchChannelError, GeoWatchChannelTopic


class GeoWatchChannelWFS(GeoWatchChannelTopic):
    """
    GeoWatchChannelWFS is used for posting GeoJSON to OGC WFS
    - topic = featuretype / layer name
    """

    @classmethod
    def encode(self, message):
        return message

    @classmethod
    def decode(self, message):
        raise GeoWatchChannelError("GeoWatch only supports sending to WFS.  GeoWatch cannot get messages from WFS.")

    def send_message(self, message, **kwargs):
        """
        message should already be converted into WFS Transaction
        """
        return self._client._make_request(data=message, contentType="text/xml", cookie=kwargs.get('cookie', None))

    def send_messages(self, messages, **kwargs):
        for message in messages:
            self._client._make_request(data=message, contentType="text/xml", cookie=kwargs.get('cookie', None))

    def get_messages_raw(self, count, block=True, timeout=5):
        raise GeoWatchChannelError("GeoWatch only supports sending to WFS.  GeoWatch cannot get messages from WFS.")

    def __init__(self, client, topic, mode, num_procs=1):
        super(GeoWatchChannelWFS, self).__init__(client, topic, mode, num_procs=num_procs)
