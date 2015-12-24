"""
This module includes base classes for GeoWatch clients
"""

# from httplib import HTTPConnection
from httplib import HTTPSConnection
from urlparse import urlsplit
import urllib2


class GeoWatchClient(object):
    """
    Base GeoWatch Client class.  Extended by others.
    """

    # Public
    backend = None
    templates = None

    def close(self):
        pass

    def __init__(self, backend="", templates=None):
        self.backend = backend
        self.templates = templates

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()


class GeoWatchClientWebHook(GeoWatchClient):

    # Public
    authtoken = None
    url_webhook = None

    def _get(self, url):
        return urllib2.urlopen(url).read()

    def _post(self, url, data):
        u2 = urlsplit(url)
        headers = {}
        conn = HTTPSConnection(u2.hostname, u2.port)
        conn.request("POST", str(u2.path), data, headers)
        response = conn.getresponse()
        return response.read()

    def __init__(self, backend="", authtoken="", url_webhook="", templates=None):
        super(GeoWatchClientWebHook, self).__init__(backend=backend, templates=templates)
        self.authtoken = authtoken
        self.url_webhook = url_webhook


class GeoWatchClientStreaming(GeoWatchClient):

    # Private
    _client = None

    def __init__(self, backend="", templates=None):
        super(GeoWatchClientStreaming, self).__init__(backend=backend, templates=templates)
        self._client = None


class GeoWatchClientTopic(GeoWatchClientStreaming):

    # Public
    topic_prefix = ""

    def wait_topic(self, topic, verbose=False):
        pass

    def __init__(self, backend="", topic_prefix="", templates=None):
        super(GeoWatchClientTopic, self).__init__(backend=backend, templates=templates)
        self.topic_prefix = topic_prefix
