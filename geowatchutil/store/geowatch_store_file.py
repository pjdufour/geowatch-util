from geowatchutil.store.base import GeoWatchStore


class GeoWatchStoreFile(GeoWatchStore):

    # Public

    # Private

    def read(self):
        return self._codec.unpack(self._get())

    def _get(self):
        message = ""
        with open(self.key, 'rb') as f:
            message = f.read()
        return message

    def _put(self, package):
        with open(self.key, 'wb') as f:
            f.write(package)

    def flush(self):
        messages = self._buffer.get_messages()
        if self.which == "first":
            self._put(self._codec.pack(messages, which=self.which))  # _codec.pack returns text representation
        elif self.which == "index":
            self._put(self._codec.pack(messages, which=self.which, which_index=self.which_index))  # _codec.pack returns text representation
        else:
            self._put(self._codec.pack(messages))  # _codec.pack returns text representation
        self._buffer.clear()

    def __init__(self, key, codec, which="all", which_index="0"):
        super(GeoWatchStoreFile, self).__init__("file", key, codec, which=which, which_index=which_index)
