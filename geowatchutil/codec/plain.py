from geowatchutil.codec import GeoWatchCodec

class GeoWatchCodecPlain(GeoWatchCodec):

    def encode(self, text=None):
        return self.encode_channel(text)

    def decode(self, text=None):
        return self.decode_channel(text)

    def __init__(self, channel=None):
        super(GeoWatchCodecPlain, self).__init__(channel=channel)
