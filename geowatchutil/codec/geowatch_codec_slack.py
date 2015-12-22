import copy
import json

from geowatchutil.codec.geowatch_codec_json import GeoWatchCodecJSON
from geowatchutil.base import GeoWatchError


class GeoWatchCodecSlack(GeoWatchCodecJSON):

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

    def encode(self, message, **kwargs):
        """
        Encode message for sending via channel
        """
        #return self.encode_channel(json.dumps(message))
        t = self._find_template(message)
        m2 = None 

        if "attachments" in t:
            m2 = copy.deepcopy(t)
            for i in range(len(m2["attachments"])):
                a = self._encode_attachment(m2["attachments"][i], message)
                m2["attachments"][i] = a
        else:
            m2 = self._render_message_plain(t, message)

        return super(GeoWatchCodecSlack, self).encode(m2)

    def _encode_attachment(self, a, message):
        """
        See: https://api.slack.com/docs/attachments
        """

        for k in ["title", "title_link", "fallback", "text", "thumb_url"]:
            if k in a:
                a[k] = a[k].format(** message)

        if "fields" in a:
            for j in range(len(a["fields"])):
                f = a["fields"][j]
                if "title" in f:
                    f["title"] = f["title"].format(** message)
                if "value" in f:
                    f["value"] = f["value"].format(** message)
                a["fields"][j].update(f)

        return copy.deepcopy(a)

    def _encode_plain(template, message):
        """
        See: https://api.slack.com/incoming-webhooks
        """

        message_encoded = None
        try:
            message_encoded = {}
            if "text" in template:
                message_encoded["text"] = template["text"].format(** message)
            if "icon_url" in template:
                message_encoded["icon_url"] = template["icon_url"].format(** message)

        except:
            print "Could not build plain slack message for resource"
            message_encoded = None

        return message_encoded

    def decode(self, message):
        """
        Decode message received via channel
        """
        raise GeoWatchError("Cannot decode slack messages.")

    def pack(self, messages, which="all", which_index=0):
        """
        pack messages for store
        """
        raise GeoWatchError("Cannot pack slack messages.")

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        raise GeoWatchError("Cannot unpack slack messages")

    def __init__(self, channel=None, templates=None):
        super(GeoWatchCodecSlack, self).__init__(channel=channel, content_type="application/json")
        self.templates = templates
