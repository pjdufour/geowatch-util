from geowatchutil.client.base import GeoWatchClientTopic


class GeoWatchClientHTTP(GeoWatchClientTopic):

    url_source = ""
    url_max = ""
    auth_user = None
    auth_password = None
    auth_b64 = None

    def _make_request(self, url=None, params=None, data=None, cookie=None, contentType=None):
        """
        Prepares a request from a url, params, and optionally authentication.
        """
        print "Data: ", data

        import urllib
        import urllib2

        if not url:
            url = self.url_source

        if params:
            url = url + '?' + urllib.urlencode(params)

        req = urllib2.Request(url, data=data)

        if self.auth_b64:
            req.add_header('AUTHORIZATION', 'Basic ' + self.auth_b64)

        if cookie:
            req.add_header('Cookie', cookie)

        if contentType:
            req.add_header('Content-type', contentType)
        else:
            if data:
                req.add_header('Content-type', 'text/xml')

        return urllib2.urlopen(req)

    def check_topic_exists(self, topic, timeout=5, verbose=True):
        return True

    def create_topic(self, topic, timeout=5, verbose=True):
        return False

    def delete_topic(self, topic, timeout=5, verbose=True):
        return False

    def delete_topics(self, topics, ignore_errors=True, timeout=5, verbose=True):
        deleted = True
        for topic in topics:
            deleted = self.delete_topic(topic, timeout=timeout, verbose=verbose)
            if (not ignore_errors) and (not deleted):
                break

        return deleted

    def list_topics(self, limit=100, verbose=True):
        """
        list_topics returns list of featuretypes
        """
        return []

    def __init__(self, backend="http", topic_prefix="", url_source="", url_max="", auth_user="", auth_password=""):
        super(GeoWatchClientHTTP, self).__init__(backend=backend, topic_prefix=topic_prefix)

        self.url_source = url_source
        self.url_max = url_max
        self.auth_user = auth_user
        self.auth_password = auth_password
        if self.auth_user and self.auth_password:
            from base64 import b64encode
            self.auth_b64 = b64encode(self.auth_user+":"+self.auth_password)
        else:
            self.auth_b64 = None
