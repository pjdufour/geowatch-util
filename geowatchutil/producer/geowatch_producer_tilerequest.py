from geowatchutil.producer.base import GeoWatchProducer, assert_now

from geowatchutil.codec.geowatch_codec_tilerequest import GeoWatchCodecTileRequest


class GeoWatchProducerTileRequest(GeoWatchProducer):

    def send_tile_requests(self, tilesource, tiles, extension='png', now=None):
        now = assert_now(now)
        messages_encoded = self._codec.encode(tilesource=tilesource, tiles=tiles, extension=extension, now=now)
        return self.send_messages(messages_encoded)

    def __init__(self, client, topic):
        super(GeoWatchProducerTileRequest, self).__init__(client, "tilerequest", topic)
