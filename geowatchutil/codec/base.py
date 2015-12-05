import json

from geowatchutil.base import parse_date, FORMAT_TILE_REQUEST
from geowatchutil.channel.geowatch_channel_file import GeoWatchChannelFile
from geowatchutil.channel.geowatch_channel_kafka import GeoWatchChannelKafka
from geowatchutil.channel.geowatch_channel_kinesis import GeoWatchChannelKinesis
from geowatchutil.channel.geowatch_channel_sns import GeoWatchChannelSNS
from geowatchutil.channel.geowatch_channel_sqs import GeoWatchChannelSQS
from geowatchutil.channel.geowatch_channel_slack import GeoWatchChannelSlack


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

    _channel = None

    def decode_channel(self, message):
        if self._channel == "file":
            return GeoWatchChannelFile.decode(message)
        elif self._channel == "kakfa":
            return GeoWatchChannelKafka.decode(message)
        elif self._channel == "kinesis":
            return GeoWatchChannelKinesis.decode(message)
        elif self._channel == "sns":
            return GeoWatchChannelSNS.decode(message)
        elif self._channel == "sqs":
            return GeoWatchChannelSQS.decode(message)
        elif self._channel == "slack":
            return GeoWatchChannelSlack.decode(message)
        else:
            return message

    def encode_channel(self, message):
        if self._channel == "file":
            return GeoWatchChannelFile.encode(message)
        elif self._channel == "kakfa":
            return GeoWatchChannelKafka.encode(message)
        elif self._channel == "kinesis":
            return GeoWatchChannelKinesis.encode(message)
        elif self._channel == "sns":
            return GeoWatchChannelSNS.encode(message)
        elif self._channel == "sqs":
            return GeoWatchChannelSQS.encode(message)
        elif self._channel == "slack":
            return GeoWatchChannelSlack.encode(message)
        else:
            return message

    def setChannel(self, channel):
        self._channel = channel

    def __init__(self, channel=None):
        self._channel = channel
