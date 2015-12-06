from geowatchutil.codec.base import GeoWatchCodec

import json


class GeoWatchCodecJSON(GeoWatchCodec):

    def encode(self, data=None):
        """
        Encode message for sending via channel
        """
        return self.encode_channel(json.dumps(data))

    def decode(self, data=None):
        """
        Decode message received via channel
        """
        return json.loads(self.decode_channel(data))

    def pack(self, messages):
        """
        pack messages for store
        """
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

    def __init__(self, channel=None):
        super(GeoWatchCodecJSON, self).__init__(channel=channel)
