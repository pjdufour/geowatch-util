from geowatchutil.channel.base import GeoWatchChannel

class GeoWatchChannelSNS(GeoWatchChannel):

    def send_message(self, message):
        self._client._client.publish(
            TopicArn=self.topic,
            Message=message)

    def send_messages(self, messages):
        for message in messages:
            self._client._client.publish(
                TopicArn=self.topic,
                Message=message)

    def get_messages_raw(self, count, block=True, timeout=5):
        return []

    def __init__(self, client, topic):
        super(GeoWatchChannelSNS, self).__init__(client)
