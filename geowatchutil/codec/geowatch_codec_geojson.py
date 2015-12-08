import json
import geojson

from geowatchutil.codec.base import GeoWatchCodec


class GeoWatchCodecGeoJSON(GeoWatchCodec):

    def encode(self, message):
        """
        Encode message for sending via channel
        - message in format FeatureCollection
        """
        return self.encode_channel(json.dumps(message))

    def decode(self, message):
        """
        Decode message received via channel
        """
        return geojson.loads(self.decode_channel(message))

    def pack(self, messages, which="all", which_index=0):
        """
        pack messages for store
        """
        if which == "first":
            return geojson.dumps(messages[0])
        elif which == "last":
            return geojson.dumps(messages[-1])
        elif which == "index":
            return geojson.dumps(messages[which_index])
        else:
            package = {
                'messages': [geojson.dumps(m) for m in messages]
            }
            return geojson.dumps(package)

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        package = geojson.loads(data)
        messages = package['mesages']
        return [geojson.loads(m) for m in messages]

    def __init__(self, channel=None):
        super(GeoWatchCodecGeoJSON, self).__init__(channel=channel, content_type="application/json")
