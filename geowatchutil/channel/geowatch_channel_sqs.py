"""
Provides :class:`GeoWatchChannelSQS`.
"""
import math

from geowatchutil.base import GeoWatchError
from geowatchutil.channel.base import GeoWatchChannel


class GeoWatchChannelSQS(GeoWatchChannel):
    """
    GeoWatchChannel for sending messages to AWS SQS
    """

    def send_message(self, message):
        self._client._client.send_message(
            QueueUrl=self.topic,
            MessageBody=message)

    def send_messages(self, messages):
        entries = [{'Id': 'message_'+str(i), 'MessageBody': messages[i]} for i in range(len(messages))]
        for i in range(len(int(entries/10))):
            self._client._client.send_message_batch(
                QueueUrl=self.topic,
                Entries=entries[(i*10):math.min((i*10+1), len(entries))])

    def get_messages_raw(self, count, block=True, timeout=5):
        if count > 10:
            raise GeoWatchError('AWS SQS can only receive at most 10 messages at once.')

        return self._client._client.receive_message(
            QueueUrl=self.topic,
            MaxNumberOfMessages=count)

    def __init__(self, client, topic):
        super(GeoWatchChannelSQS, self).__init__(client)
