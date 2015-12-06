class GeoWatchBuffer(object):

    # Public
    limit = None

    # Private
    _count = None
    _messages = []

    def add_message(self, message):
        self.messages.append(message)

    def add_messages(self, messages):
        self.messages.extend(messages)

    def get_messages(self):
        return self.messages

    def full(self):
        if self.limit > 0:
            return len(self._messages) > self.limit
        else:
            return False

    def clear(self):
        self.messages = []

    def __init__(self, limit=0):
        self.limit = limit
        self.messages = []
