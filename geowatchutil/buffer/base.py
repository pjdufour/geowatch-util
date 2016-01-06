class GeoWatchBuffer(object):

    # Public
    limit = None
    check_limit = False

    # Private
    _messages = []

    def add_message(self, message):
        if self.check_limit:
            if not self.full():
                self._messages.append(message)
            else:
                raise GeoWatchBufferError("The new message would have exceeded the buffer's limit of "+self.limit+".")
        else:
            self._messages.append(message)

    def add_messages(self, messages):
        if self.check_limit:
            if self.size() + len(messages) <= self.limit:
                self._messages.extend(messages)
            else:
                raise GeoWatchBufferError("The new messages would have exceeded the buffer's limit of "+self.limit+".")
        else:
            self._messages.extend(messages)

    def get_messages(self):
        return self._messages

    def pop_messages(self, count):
        if count >= self.size():
            r = self._messages
            self.clear()
            return r
        else:
            r = self._messages[:count]
            self._messages = self._messages[count:]
            return r

    def full(self):
        if self.limit > 0:
            return len(self._messages) >= self.limit
        else:
            return False

    def empty(self):
        return len(self._messages) == 0

    def size(self):
        return len(self._messages)

    def clear(self):
        self._messages = []

    def __init__(self, limit=0, check_limit=False):
        self.limit = limit
        self.check_limit = check_limit
        self._messages = []


class GeoWatchBufferError(Exception):

    def __init__(self, * args, ** kwargs):
        super(GeoWatchBufferError, self).__init__(self, * args, ** kwargs)
