from geowatchutil.codec.base import GeoWatchCodec


class GeoWatchCodecPlain(GeoWatchCodec):
    """
    GeoWatchCodecPlain is used for encoding/decoding packaing/unpacking plain text
    """

    def encode(self, text=None):
        """
        Encode for sending via channel
        """
        return self.encode_channel(text)

    def decode(self, text=None):
        """
        Decode messages received via channel
        """
        return self.decode_channel(text)

    def pack(self, messages):
        """
        pack messages for store
        """
        return "\n".join(messages)

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        return data.split("\n")

    def __init__(self, channel=None):
        super(GeoWatchCodecPlain, self).__init__(channel=channel)
