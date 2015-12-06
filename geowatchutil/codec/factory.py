from geowatchutil.codec.plain import GeoWatchCodecPlain
from geowatchutil.codec.json import GeoWatchCodecJSON
from geowatchutil.codec.tilerequest import GeoWatchCodecTileRequest


def build_codec(codec, channel=None):
    """
    build_codec returns a GeoWatchCodec object based on well-known name
    """
    codec_lc = codec.lower()
    if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
        return GeoWatchCodecTileRequest(channel=channel)
    elif codec_lc == "json" or codec_lc == "geowatchcodecjson":
        return GeoWatchCodecJSON(channel=channel)
    else:
        return GeoWatchCodecPlain(channel=channel)
