from geowatchutil.store.base import GeoWatchStoreWebHook
from geowatchutil.base import GeoWatchError


class GeoWatchStoreWFS(GeoWatchStoreWebHook):

    def read(self):
        raise GeoWatchError("Cannot decode wfs messages.")

    def _get(self):
        raise GeoWatchError("Cannot decode wfs messages.")

    def _put(self, data, **kwargs):
        return self._make_request(
            params=None,
            data=data,
            cookie=kwargs.get('cookie', None),
            contentType=kwargs.get('contentType', None))

    def flush(self, **kwargs):
        response = None
        messages = self._buffer.get_messages()
        if self.which == "first":
            response = self._put(self._codec.pack(messages, key=self.key, which=self.which), **kwargs)
        elif self.which == "index":
            response = self._put(self._codec.pack(messages, key=self.key, which=self.which, which_index=self.which_index), **kwargs)
        else:
            response = self._put(self._codec.pack(messages, key=self.key), **kwargs)
        self._buffer.clear()
        return response

    def close(self):
        pass

    def __init__(self, key, codec, url=None, auth_user=None, auth_password=None, which="all", which_index=0):
        super(GeoWatchStoreWFS, self).__init__(
            "wfs",
            key,
            codec,
            url=url,
            auth_user=auth_user,
            auth_password=auth_password,
            which=which,
            which_index=which_index)
