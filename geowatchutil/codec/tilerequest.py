from geowatchutil.codec import GeoWatchCodec

from geowatchutil.base import parse_date, FORMAT_TILE_REQUEST

class GeoWatchCodecTileRequest(GeoWatchCodec):

    def encode(self, tilesource=None, tiles=None, extension=None, now=None):
        messages = []
        for tile in tiles:
            x, y, z = tile
            message = FORMAT_TILE_REQUEST.format(d=now.isoformat(), tilesource=tilesource, z=str(z), x=str(x), y=str(y), ext=extension)
            messages.append(self.encode_channel(message))
        return messages

    def decode(self):
        pass

    def __init__(self, channel=None):
        super(GeoWatchCodecTileRequest, self).__init__(channel=channel)
