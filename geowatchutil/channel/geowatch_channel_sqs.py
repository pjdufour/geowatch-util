from geowatchutil.channel.base import GeoWatchChannel

class GeoWatchChannelSQS(GeoWatchChannel):

    def send_message(self, message):
        self._client._client.publish(
            TopicArn=self.topic,
            MessageBody=message)

    def send_messages(self, messages):
        for message in messages:
            self._client._client.publish(
                TopicArn=self.topic,
                MessageBody=message)

    def get_messages_raw(self, count, block=True, timeout=5):
        return []

    def __init__(self, client, topic):
        super(GeoWatchChannelSQS, self).__init__(client)
