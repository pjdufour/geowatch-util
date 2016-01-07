from geowatchutil.codec.base import GeoWatchCodec

import json


class GeoWatchCodecJSON(GeoWatchCodec):

    def encode(self, message, **kwargs):
        """
        Encode message for sending via channel
        """
        return self.encode_channel(json.dumps(message))

    def decode(self, message):
        """
        Decode message received via channel
        """
        m2 = self.decode_channel(message)
        # Don't decode if already JSON, which can happen with sockets, such as Slack RTM
        return json.loads(m2) if isinstance(m2, basestring) else m2 

    def pack(self, messages, which="all", which_index=0):
        """
        pack messages for store
        """
        if which == "first":
            return json.dumps(messages[0])
        elif which == "last":
            return json.dumps(messages[-1])
        elif which == "index":
            return json.dumps(messages[which_index])
        else:
            package = {
                'messages': [json.dumps(m) for m in messages]
            }
            return json.dumps(package)

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        package = json.loads(data)
        messages = package['mesages']
        return [json.loads(m) for m in messages]

    def __init__(self, channel=None, content_type="application/json"):
        super(GeoWatchCodecJSON, self).__init__(channel=channel, content_type=content_type)
