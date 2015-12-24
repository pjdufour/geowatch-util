from geowatchutil.base import parse_date


def decode_tile_request(a):
    b = a.split(",")
    return {
        'layer': b[0],
        'z': int(b[1]),
        'x': int(b[2]),
        'y': int(b[3]),
        'extension': b[4]
    }


def decode_tile_request_log(a):
    b = a.split("\t")
    return {
        'status': b[0],
        'tileorigin': b[1],
        'tilesource': b[2],
        'z': int(b[3]),
        'x': int(b[4]),
        'y': int(b[5]),
        'extension': b[6],
        'ip': b[7],
        'datetime': parse_date(b[8])
    }


class GeoWatchCodec(object):

    # Public
    content_type = "text/plain"
    templates = None

    # Private
    _channel = None

    def decode_channel(self, message):
        if self._channel == "file":
            from geowatchutil.channel.geowatch_channel_file import GeoWatchChannelFile
            return GeoWatchChannelFile.decode(message)
        elif self._channel == "kakfa":
            from geowatchutil.channel.geowatch_channel_kafka import GeoWatchChannelKafka
            return GeoWatchChannelKafka.decode(message)
        elif self._channel == "kinesis":
            from geowatchutil.channel.geowatch_channel_kinesis import GeoWatchChannelKinesis
            return GeoWatchChannelKinesis.decode(message)
        elif self._channel == "sns":
            from geowatchutil.channel.geowatch_channel_sns import GeoWatchChannelSNS
            return GeoWatchChannelSNS.decode(message)
        elif self._channel == "sqs":
            from geowatchutil.channel.geowatch_channel_sqs import GeoWatchChannelSQS
            return GeoWatchChannelSQS.decode(message)
        elif self._channel == "slack":
            from geowatchutil.channel.geowatch_channel_slack import GeoWatchChannelSlack
            return GeoWatchChannelSlack.decode(message)
        elif self._channel == "wfs":
            from geowatchutil.channel.geowatch_channel_wfs import GeoWatchChannelWFS
            return GeoWatchChannelWFS.decode(message)
        else:
            return message

    def encode_channel(self, message):
        if self._channel == "file":
            from geowatchutil.channel.geowatch_channel_file import GeoWatchChannelFile
            return GeoWatchChannelFile.encode(message)
        elif self._channel == "kakfa":
            from geowatchutil.channel.geowatch_channel_kafka import GeoWatchChannelKafka
            return GeoWatchChannelKafka.encode(message)
        elif self._channel == "kinesis":
            from geowatchutil.channel.geowatch_channel_kinesis import GeoWatchChannelKinesis
            return GeoWatchChannelKinesis.encode(message)
        elif self._channel == "sns":
            from geowatchutil.channel.geowatch_channel_sns import GeoWatchChannelSNS
            return GeoWatchChannelSNS.encode(message)
        elif self._channel == "sqs":
            from geowatchutil.channel.geowatch_channel_sqs import GeoWatchChannelSQS
            return GeoWatchChannelSQS.encode(message)
        elif self._channel == "slack":
            from geowatchutil.channel.geowatch_channel_slack import GeoWatchChannelSlack
            return GeoWatchChannelSlack.encode(message)
        elif self._channel == "wfs":
            from geowatchutil.channel.geowatch_channel_wfs import GeoWatchChannelWFS
            return GeoWatchChannelWFS.encode(message)
        else:
            return message

    def find_template(self, message):
        t = None
        for candidate in self.templates:
            print "GeoWatchCodec.find_templates candidate: ", candidate
            action = message["template"]["actiontype"]
            resource = message["template"]["resourcetype"]
            if action in candidate["actions"] and resource in candidate["resources"]:
                t = candidate["template"]
                break
        return t

    def __init__(self, channel=None, content_type="text/plain", templates=None):
        self._channel = channel
        self.content_type = content_type
        self.templates = templates
