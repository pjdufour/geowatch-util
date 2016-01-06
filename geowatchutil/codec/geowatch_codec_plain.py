import copy

from geowatchutil.base import GeoWatchError
from geowatchutil.codec.base import GeoWatchCodec


class GeoWatchCodecPlain(GeoWatchCodec):
    """
    GeoWatchCodecPlain is used for encoding/decoding packaing/unpacking plain text
    """

    def encode(self, message, **kwargs):
        """
        Encode for sending via channel
        """
        return self.encode_channel(message)

    def decode(self, message):
        """
        Decode messages received via channel
        """
        return self.decode_channel(message)

    def pack(self, messages, which="all", which_index=0):
        """
        pack messages for store
        """
        if which == "first":
            return messages[0]
        elif which == "last":
            return messages[-1]
        elif which == "index":
            return messages[which_index]
        else:
            return "\n".join(messages)

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        return data.split("\n")

    def render(self, message):
        """
        Render template for sending via channel
        """
        t = self.find_template(message)
        if not t:
            raise GeoWatchError("GeoWatchCodecPlain.render: Could not find template.")
        if 'metadata' in message:
            return self.encode_channel(copy.deepcopy(t).format(** message['data']))
        else:
            return self.encode_channel(copy.deepcopy(t).format(** message))

    def __init__(self, channel=None, content_type="text/plain", templates=None):
        super(GeoWatchCodecPlain, self).__init__(channel=channel, content_type=content_type, templates=templates)
