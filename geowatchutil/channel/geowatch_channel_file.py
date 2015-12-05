from geowatchutil.channel.base import GeoWatchChannel

class GeoWatchChannelFile(GeoWatchChannel):

    _file = None

    @classmethod
    def encode(self, message):
        return message

    @classmethod
    def decode(self, message):
        return message

    def send_message(self, message):
        self._file.write(message+"\n")
        self._file.flush()

    def send_messages(self, messages):
        for message in messages:
            self._file.write(message+"\n")
        self._file.flush()

    def get_messages_raw(self, count):
        messages = []
        for i in range(count):
            line = self._file.readline()
            if line:
                messages.append(line)
            else:  # EOF
                break
        return messages

    def close(self):
        self._file.close()

    def __init__(self, client, mode):
        super(GeoWatchChannelFile, self).__init__(client, mode, num_procs=1)

        if mode == "duplex":
            self._file = open(self._client.path, 'r+b')
        elif mode == "producer":
            self._file = open(self._client.path, 'ab')
        elif mode == "consumer":
            self._file = open(self._client.path, 'rb')
