from geowatchutil.codec.base import GeoWatchCodec

from geowatchutil.base import FORMAT_TILE_REQUEST


class GeoWatchCodecTileRequest(GeoWatchCodec):

    def encode(self, tilesource=None, tiles=None, extension=None, now=None):
        messages = []
        for tile in tiles:
            x, y, z = tile
            message = FORMAT_TILE_REQUEST.format(d=now.isoformat(), tilesource=tilesource, z=str(z), x=str(x), y=str(y), ext=extension)
            messages.append(self.encode_channel(message))
        return messages

    def decode(self, message):
        """
        Decode messages received via channel
        """
        print "This should never be called.  Decode tile requests in consumers"
        return None

    def pack(self, tilesource=None, tiles=None, extension=None, now=None):
        """
        pack messages for store
        """
        messages = []
        for tile in tiles:
            x, y, z = tile
            message = FORMAT_TILE_REQUEST.format(d=now.isoformat(), tilesource=tilesource, z=str(z), x=str(x), y=str(y), ext=extension)
            messages.append(message)
        return "\n".join(messages)

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        return data.split("\n")

    def __init__(self, channel=None):
        super(GeoWatchCodecTileRequest, self).__init__(channel=channel)
