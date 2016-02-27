from geowatchutil.codec.base import GeoWatchCodec

import json

import defusedxml.ElementTree as et

class GeoWatchCodecXML(GeoWatchCodec):

    def encode(self, message, **kwargs):
        """
        Encode message for sending via channel
        """
        return self.encode_channel(et.tostring(message))

    def decode(self, message):
        """
        Decode message received via channel
        """
        m2 = self.decode_channel(message)
        # Don't decode if already JSON, which can happen with sockets, such as Slack RTM
        return et.fromstring(m2) if isinstance(m2, basestring) else m2

    def pack(self, messages, which="all", which_index=0):
        """
        pack messages for store
        """
        if which == "first":
            return et.tostring(messages[0])
        elif which == "last":
            return et.tostring(messages[-1])
        elif which == "index":
            return et.tostring(messages[which_index])
        else:
            return "\n".join([et.tostring(m) for m in messages])

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        messages = data.split("\n")
        return [et.fromstring(m) for m in messages]

    def __init__(self, channel=None, content_type="text/xml"):
        super(GeoWatchCodecXML, self).__init__(channel=channel, content_type=content_type)
