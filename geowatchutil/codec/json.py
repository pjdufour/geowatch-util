from geowatchutil.codec import GeoWatchCodec

class GeoWatchCodecJSON(GeoWatchCodec):

    def encode(self, data=None):
        return self.encode_channel(json.dumps(data))

    def decode(self):
        pass

    def __init__(self, channel=None):
        super(GeoWatchCodecJSON, self).__init__(channel=channel)
