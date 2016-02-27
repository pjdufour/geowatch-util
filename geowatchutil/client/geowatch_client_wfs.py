from geowatchutil.client.geowatch_client_http import GeoWatchClientHTTP

class GeoWatchClientWFS(GeoWatchClientHTTP):

    def __init__(self, topic_prefix="", url_source="", auth_user="", auth_password=""):
        super(GeoWatchClientWFS, self).__init__(
            backend="osm",
            topic_prefix=topic_prefix,
            url_source=url_source,
            auth_user=auth_user,
            auth_password=auth_password)
