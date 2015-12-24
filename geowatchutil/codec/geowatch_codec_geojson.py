import json
import geojson

from geojson.mapping import to_mapping

from geowatchutil.codec.base import GeoWatchCodec


class GeoWatchCodecGeoJSON(GeoWatchCodec):

    def encode(self, message, **kwargs):
        """
        Encode message for sending via channel
        - message in format FeatureCollection
        """
        if "metadata" in message:
            message["data"] = to_mapping(message["data"])
            print message
            return self.encode_channel(json.dumps(message))
        else:
            return self.encode_channel(geojson.dumps(message))

    def decode(self, message):
        """
        Decode message received via channel
        """
        message_decoded = self.decode_channel(message)
        message_json = json.loads(message_decoded)
        if "metadata" in message_json:
            message_json["data"] = geojson.loads(json.dumps(message_json["data"]))
            return message_json
        else:
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
                'messages': [to_mapping(m) for m in messages]
            }
            return json.dumps(package)

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        package = geojson.loads(data)
        messages = package['mesages']
        return [geojson.loads(m) for m in messages]

    def __init__(self, channel=None, content_type="application/json"):
        super(GeoWatchCodecGeoJSON, self).__init__(channel=channel, content_type=content_type)
