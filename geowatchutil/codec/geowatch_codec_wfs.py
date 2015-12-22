import copy
import json

from geowatchutil.codec.geowatch_codec_geojson import GeoWatchCodecGeoJSON
from geowatchutil.base import GeoWatchError


class GeoWatchCodecWFS(GeoWatchCodecGeoJSON):

    def _build_transaction(self, default_featuretype, messages):
        t = '<?xml version="1.0" encoding="UTF-8"?>\n'
        t = t + '<wfs:Transaction xmlns:geonode="http://www.geonode.org/" xmlns:wfs="http://www.opengis.net/wfs" xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" service= "WFS" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd">\n'
        for message in messages:
            ft = None
            data = None
            if 'metadata' in message:
                ft = message['metadata'].get('featuretype', default_featuretype)
                data = message['data']
            else:
                ft = default_featuretype
                data = message
            if ft and data:
                t = t + '    <wfs:Insert>\n'
                if 'features' in data:
                    for f in data['features']:
                        t = t + '    <'+ ft +">\n"
                        for k in f['properties']:
                            if f['properties'][k]:
                                t = t + '      <'+k+'>'+str(f['properties'][k])+'</'+k+'>\n'
                        t = t + '      <'+f['geometry_name']+'>\n'
                        if f['geometry']['type'] == "Point":
                            t = t + '      <gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#4326"><gml:coordinates decimal="." cs="," ts=" ">'+(str(f['geometry']['coordinates'][0])+","+str(f['geometry']['coordinates'][1]))+'</gml:coordinates></gml:Point>\n'
                        t = t + '    </'+f['geometry_name']+'>\n'
                        t = t + '    </'+ ft +">\n"
                t = t + '  </wfs:Insert>\n'
        t = t + '</wfs:Transaction>'
        return t

    def encode(self, message, **kwargs):
        """
        Encode message for sending via channel
        """
        return self._build_transaction(kwargs.get('topic', None), [message])

    def decode(self, message):
        """
        Decode message received via channel
        """
        raise GeoWatchError("Cannot decode wfs messages.")

    def pack(self, messages, **kwargs):
        """
        pack messages for store
        """
        which = kwargs.get('which', None)
        which_index = kwargs.get('which_index', 0)
        key = kwargs.get('key', None)

        if which == "first":
            return self._build_transaction(key, messages[:1])
        elif which == "last":
            return self._build_transaction(key, messages[-1:])
        elif which == "index":
            return self._build_transaction(key, messages[which_index:(which_index+1)])
        else:
            return self._build_transaction(key, messages)

    def unpack(self, data):
        """
        unpack data from store into messages
        """
        raise GeoWatchError("Cannot unpack wfs messages")

    def __init__(self, channel=None):
        super(GeoWatchCodecWFS, self).__init__(channel=channel, content_type="application/xml")
