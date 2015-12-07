from geowatchutil.store.base import GeoWatchStore


class GeoWatchStoreMemcached(GeoWatchStore):

    # Public
    client_type = None

    # Private
    _client = None

    def read(self):
        return self._codec.unpack(self._get())

    def _get(self):
        if self.client_type == "umemcache":
            return self._client.get(self.key)
        elif self.client_type == "pymemcache":
            return self._client.get(self.key)
        else:
            return None

    def _put(self, package):
        if self.client_type == "umemcache":
            return self._client.set(self.key, package)
        elif self.client_type == "pymemcache":
            return self._client.set(self.key, package)
        else:
            return None

    def flush(self):
        messages = self._buffer.get_messages()
        self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def __init__(self, key, codec, host=None, port=None, client_type="pymemcache", which="all", which_index=0):
        super(GeoWatchStoreMemcached, self).__init__("memcached", key, codec, which, which_index)
        self.client_type = client_type
        if host and port:
            if self.client_type == "umemcache":
                # try:
                if 1 == 1:
                    cache_params = {
                        'BACKEND': 'memcachepool.cache.UMemcacheCache',
                        'LOCATION': host+":"+str(port),
                        'OPTIONS': {
                            'MAX_POOL_SIZE': 40,
                            'BLACKLIST_TIME': 60,
                            'SOCKET_TIMEOUT': 60,
                            'MAX_ITEM_SIZE': 1000*1000*1000
                        }
                    }
                    # from umemcache import MemcachedError
                    from memcachepool.cache import UMemcacheCache
                    self._client = UMemcacheCache(host+":"+str(port), cache_params)
                # except:
                #    self._client = None
            elif self.client_type == "pymemcache":
                try:
                    from pymemcache.client.base import Client
                    self._client = Client((host, port), default_noreply=False)  # Set default_noreply to not wait for response
                except:
                    self._client = None
        else:
            print "Could not create GeoWatch client for S3 Backend.  Missing parameters."
