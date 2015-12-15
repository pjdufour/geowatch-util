import copy
import json

from geowatchutil.codec.geowatch_codec_plain import GeoWatchCodecPlain
from geowatchutil.base import GeoWatchError


class GeoWatchCodecTemplated(GeoWatchCodecPlain):

    templates = None

    def _find_template(self, message):
        t = None
        for candidate in self.templates:
            print "candidate: ", candidate
            action = message["template"]["actiontype"]
            resource = message["template"]["resourcetype"]
            if action in candidate["actions"] and resource in candidate["resources"]:
                t = candidate["template"]
                break
        return t

    def encode(self, message):
        """
        Encode message for sending via channel
        """
        t = self._find_template(message)
        print "template: ", t
        return super(GeoWatchCodecTemplated, self).encode(copy.deepcopy(t).format(** message))

    def decode(self, message):
        """
        Decode message received via channel
        """
        raise GeoWatchError("Cannot decode templated messages.")

    def pack(self, messages, which="all", which_index=0):
        """
        pack messages for store
        """
        raise GeoWatchError("Cannot pack templated messages.")

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        raise GeoWatchError("Cannot unpack templated messages")

    def __init__(self, channel=None, templates=None):
        super(GeoWatchCodecTemplated, self).__init__(channel=channel, content_type="text/plain")
        self.templates = templates
