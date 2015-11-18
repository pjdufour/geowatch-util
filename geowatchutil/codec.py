import json

from geowatchutil.base import parse_date, FORMAT_TILE_REQUEST
from geowatchutil.channel import GeoWatchChannelFile, GeoWatchChannelKafka, GeoWatchChannelKinesis


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
        else:
            return message

    def encode_channel(self, message):
        if self._channel == "file":
            return GeoWatchChannelFile.encode(message)
        elif self._channel == "kakfa":
            return GeoWatchChannelKafka.encode(message)
        elif self._channel == "kinesis":
            return GeoWatchChannelKinesis.encode(message)
        else:
            return message

    def setChannel(self, channel):
        self._channel = channel

    def __init__(self, channel=None):
        self._channel = channel


class GeoWatchCodecPlain(GeoWatchCodec):

    def encode(self, text=None):
        return self.encode_channel(text)

    def decode(self, text=None):
        return self.decode_channel(text)

    def __init__(self, channel=None):
        super(GeoWatchCodecPlain, self).__init__(channel=channel)


class GeoWatchCodecTileRequest(GeoWatchCodec):

    def encode(self, tilesource=None, tiles=None, extension=None, now=None):
        messages = []
        for tile in tiles:
            x, y, z = tile
            message = FORMAT_TILE_REQUEST.format(d=now.isoformat(), tilesource=tilesource, z=str(z), x=str(x), y=str(y), ext=extension)
            messages.append(self.encode_channel(message))
        return messages

    def decode(self):
        pass

    def __init__(self, channel=None):
        super(GeoWatchCodecTileRequest, self).__init__(channel=channel)


class GeoWatchCodecJSON(GeoWatchCodec):

    def encode(self, data=None):
        return self.encode_channel(json.dumps(data))

    def decode(self):
        pass

    def __init__(self, channel=None):
        super(GeoWatchCodecJSON, self).__init__(channel=channel)
