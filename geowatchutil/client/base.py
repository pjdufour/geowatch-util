# from httplib import HTTPConnection
from httplib import HTTPSConnection
from urlparse import urlsplit


class GeoWatchClient(object):

    # Public
    backend = None

    def __init__(self, backend=""):
        self.backend = backend


class GeoWatchClientWebHook(GeoWatchClient):

    # Public
    authtoken = None
    url_webhook = None

    def _get(url):
        u2 = urlsplit(url)
        headers = {}
        conn = HTTPSConnection(u2.hostname, u2.port)
        conn.request("GET", str(u2.path), None, headers)
        response = conn.getresponse()
        return response.read()

    def _post(url, data):
        u2 = urlsplit(url)
        headers = {}
        conn = HTTPSConnection(u2.hostname, u2.port)
        conn.request("POST", str(u2.path), data, headers)
        response = conn.getresponse()
        return response.read()

    def __init__(self, backend="", authtoken="", url_webhook=""):
        super(GeoWatchClientWebHook, self).__init__(backend=backend)
        self.authtoken = authtoken
        self.url_webhook = url_webhook


class GeoWatchClientStreaming(GeoWatchClient):

    # Private
    _client = None

    def __init__(self, backend=""):
        super(GeoWatchClientStreaming, self).__init__(backend=backend)
        self._client = None


class GeoWatchClientTopic(GeoWatchClientStreaming):

    # Public
    topic_prefix = ""

    def __init__(self, backend="", topic_prefix=""):
        super(GeoWatchClientTopic, self).__init__(backend=backend)
        self.topic_prefix = topic_prefix
