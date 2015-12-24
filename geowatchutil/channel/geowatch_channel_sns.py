from geowatchutil.channel.base import GeoWatchChannelError, GeoWatchChannelTopic


class GeoWatchChannelSNS(GeoWatchChannelTopic):

    @classmethod
    def encode(self, message):
        return message

    @classmethod
    def decode(self, message):
        raise GeoWatchChannelError("GeoWatch only supports sending to SNS.  GeoWatch cannot get messages from SNS.")

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
        raise GeoWatchChannelError("GeoWatch only supports sending to SNS.  GeoWatch cannot get messages from SNS.")

    def __init__(self, client, topic, mode, num_procs=1):
        super(GeoWatchChannelSNS, self).__init__(client, topic, mode, num_procs=num_procs)
