from geowatchutil.channel.base import GeoWatchChannelTopic


class GeoWatchChannelSlack(GeoWatchChannelTopic):

    # Public

    # Private

    @classmethod
    def encode(self, message):
        return message

    @classmethod
    def decode(self, message):
        return message

    def send_message(self, message):
        partition_key = message[:256]
        self._client._client.put_record(
            StreamName=(self._client.topic_prefix + self.topic),
            Data=message,
            PartitionKey=partition_key)

    def send_messages(self, messages):
        records = []
        for message in messages:
            partition_key = message[:256]
            records.append({'Data': message, 'PartitionKey': partition_key})
        self._client._client.put_records(Records=records, StreamName=(self._client.topic_prefix + self.topic))

    def get_messages_raw(self, count, block=True, timeout=5):
        return self._client._client.get_records(ShardIterator=self._shard_it, Limit=count)

    def __init__(self, client, topic, mode, num_procs=1, ):
        super(GeoWatchChannelSlack, self).__init__(client, topic, mode, num_procs=num_procs)
