from geowatchutil.buffer.base import GeoWatchBuffer
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

    def write_message(self, message, flush=False):
        self._buffer.add_message(message)
        if flush:
            self.flush()

    def write_messages(self, messages, flush=False):
        self._buffer.add_messages(messages)
        if flush:
            self.flush()

    def __init__(self, backend, key, codec, which="all", which_index=0):
        self.backend = backend
        self.key = key
        self._buffer = GeoWatchBuffer()
        self._codec = build_codec(codec)  # takes in well-known codec name and returns object
        self.which = which
        self.which_index = which_index
