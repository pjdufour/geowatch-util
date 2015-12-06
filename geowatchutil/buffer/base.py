class GeoWatchBuffer(object):

    # Public
    max_count = None

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
        return self._count > self.limit

    def clear(self):
        self.messages = []

    def __init__(self, limit):
        self.limit = limit
        self.messages = []
