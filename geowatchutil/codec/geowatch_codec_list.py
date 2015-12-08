from geowatchutil.codec.base import GeoWatchCodec


class GeoWatchCodecList(GeoWatchCodec):
    """
    GeoWatchCodecList is used for encoding/decoding and packaging/unpacking lists.
    """

    separator = "\t"

    def encode(self, message):
        """
        Encode for sending via channel
        """
        return self.encode_channel(self.separator.join(message))

    def decode(self, message):
        """
        Decode messages received via channel
        """
        return self.decode_channel(message).split(self.separator)

    def pack(self, messages, which="all", which_index=0):
        """
        pack messages for store
        """
        if which == "first":
            return self.separator.join(messages[0])
        elif which == "last":
            return self.separator.join(messages[-1])
        elif which == "index":
            return self.separator.join(messages[which_index])
        else:
            return "\n".join([self.separator.join(m) for m in messages])

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        return [m.split(self.separator) for m in data.split("\n")]

    def __init__(self, channel=None, separator="\t"):
        super(GeoWatchCodecList, self).__init__(channel=channel, content_type="text/plain")
        this.separator = separator
