def build_codec(codec, channel=None, templates=None):
    """
    build_codec returns a GeoWatchCodec object based on well-known name
    """
    codec_lc = codec.lower()
    if codec_lc == "tile_request" or codec_lc == "tilerequest" or codec_lc == "geowatchcodectilerequest":
        from geowatchutil.codec.geowatch_codec_tilerequest import GeoWatchCodecTileRequest
        return GeoWatchCodecTileRequest(channel=channel)
    elif codec_lc == "json" or codec_lc == "geowatchcodecjson":
        from geowatchutil.codec.geowatch_codec_json import GeoWatchCodecJSON
        return GeoWatchCodecJSON(channel=channel)
    elif codec_lc == "list" or codec_lc == "geowatchcodeclist":
        from geowatchutil.codec.geowatch_codec_list import GeoWatchCodecList
        return GeoWatchCodecList(channel=channel, separator="\t")
    elif codec_lc == "geojson" or codec_lc == "geowatchcodecgeojson":
        from geowatchutil.codec.geowatch_codec_geojson import GeoWatchCodecGeoJSON
        return GeoWatchCodecGeoJSON(channel=channel)
    elif codec_lc == "slack" or codec_lc == "geowatchcodecslack":
        from geowatchutil.codec.geowatch_codec_slack import GeoWatchCodecSlack
        return GeoWatchCodecSlack(channel=channel, templates=templates)
    elif codec_lc == "wfs" or codec_lc == "geowatchcodecwfs":
        from geowatchutil.codec.geowatch_codec_wfs import GeoWatchCodecWFS
        return GeoWatchCodecWFS(channel=channel)
    elif codec_lc == "xml" or codec_lc == "geowatchcodecxml":
        from geowatchutil.codec.geowatch_codec_xml import GeoWatchCodecXML
        return GeoWatchCodecXML(channel=channel)
    else:
        from geowatchutil.codec.geowatch_codec_plain import GeoWatchCodecPlain
        return GeoWatchCodecPlain(channel=channel, templates=templates)
