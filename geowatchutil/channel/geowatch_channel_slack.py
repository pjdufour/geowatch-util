import copy

from geowatchutil.buffer.base import GeoWatchBuffer
from geowatchutil.channel.base import GeoWatchChannelTopic, GeoWatchChannelError


class GeoWatchChannelSlack(GeoWatchChannelTopic):

    # Public
    message_templates = None

    # Private
    _buffer = None  # Used for temporarily caching messages locally since rtm returns all messages

    @classmethod
    def encode(self, message):
        return message

    @classmethod
    def decode(self, message):
        return message

    def _render_message_attachments(self, m, t):
        """
        render message based on template
        """
        r = copy.deepcopy(t)
        for i in range(len(r["attachments"])):
            a = self._render_message_attachment(m, r["attachments"][i])
            r["attachments"][i] = a
        return r

    def _render_message_attachment(self, m, a):
        r = copy.deepcopy(a)
        for k in ["title", "title_link", "fallback", "text", "thumb_url"]:
            if k in r:
                r[k] = r[k].format(** m)

        if "fields" in r:
            for j in range(len(r["fields"])):
                f = r["fields"][j]
                if "title" in f:
                    f["title"] = f["title"].format(** m)
                if "value" in f:
                    f["value"] = f["value"].format(** m)
                r["fields"][j].update(f)

        return r

    def _render_message_plain(self, m, t):
        r = None
        try:
            r = {}
            if "text" in t:
                r["text"] = t["text"].format(** m)
            if "icon_url" in t:
                r["icon_url"] = t["icon_url"].format(** m)

        except:
            print "Could not build plain slack message for resource"
            r = None

        return r

    def send_message(self, message):
        return self._client._post(self._client.url_webhook, message)

    def send_messages(self, messages):
        for message in messages:
            return self._client._post(self._client.url_webhook, message)

    def get_messages_raw(self, count, block=True, timeout=5):
        if self._client:
            self._buffer.add_messages(self._client._client.rtm_read())
            return self._buffer.pop_messages(count=count)
        else:
            raise GeoWatchChannelError("Client has not been initialized for GeoWatch Slack channel")

    def __init__(self, client, topic, mode, num_procs=1, message_templates=None):
        super(GeoWatchChannelSlack, self).__init__(
            client,
            topic,
            mode,
            num_procs=num_procs)
        self.message_templates = message_templates

        if mode == "duplex" or mode == "consumer":
            self._client._client.rtm_connect()
            self._buffer = GeoWatchBuffer()
