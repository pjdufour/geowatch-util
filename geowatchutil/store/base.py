from geowatchutil.buffer.base import GeoWatchBufferLocalMemory
from geowatchutil.codec.factory import build_codec


class GeoWatchStore(object):

    # Public
    backend = None
    key = None  # or path
    which = None
    which_index = None

    # Private
    _buffer = None  # Used for temporarily caching messages locally before storing
    _codec = None

    def write_message(self, message, flush=False, flush_kwargs=None):
        self._buffer.add_message(message)
        if flush:
            return self.flush(**flush_kwargs)
        else:
            return True

    def write_messages(self, messages, flush=False, flush_kwargs=None):
        self._buffer.add_messages(messages)
        if flush:
            return self.flush(**flush_kwargs)
        else:
            return True

    def close(self):
        pass

    def __init__(self, backend, key, codec, which="all", which_index=0):
        self.backend = backend
        self.key = key
        self._buffer = GeoWatchBufferLocalMemory()
        self._codec = build_codec(codec)  # takes in well-known codec name and returns object
        self.which = which
        self.which_index = which_index

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()


class GeoWatchStoreWebHook(GeoWatchStore):

    url = ""
    auth_user = None
    auth_password = None
    auth_b64 = None

    def _make_request(self, params=None, data=None, cookie=None, contentType=None):
        """
        Prepares a request from a url, params, and optionally authentication.
        """
        print "Data: ", data

        import urllib
        import urllib2

        url = self.url
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

    def __init__(self, backend, key, codec, url=None, auth_user=None, auth_password=None, which="all", which_index=0):
        super(GeoWatchStoreWebHook, self).__init__(backend, key, codec, which=which, which_index=which_index)
        self.url = url
        self.auth_user = auth_user
        self.auth_password = auth_password
        if self.auth_user and self.auth_password:
            from base64 import b64encode
            self.auth_b64 = b64encode(self.auth_user+":"+self.auth_password)
        else:
            self.auth_b64 = None
