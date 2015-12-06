from geowatchutil.channel.base import GeoWatchChannel


class GeoWatchChannelSlack(GeoWatchChannel):

    def send_message(self, message):
        pass

    def send_messages(self, messages):
        for message in messages:
            pass

    def get_messages_raw(self, count, block=True, timeout=5):
        return []

    def __init__(self, client, topic):
        super(GeoWatchChannelSlack, self).__init__(client)
