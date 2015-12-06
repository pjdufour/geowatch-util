from geowatchutil.channel.base import GeoWatchChannelTopic


class GeoWatchChannelKinesis(GeoWatchChannelTopic):

    # Public
    shard_it_type = 'LATEST'
    # AT_SEQUENCE_NUMBER - Start reading exactly from the position denoted by a specific sequence number.
    # AFTER_SEQUENCE_NUMBER - Start reading right after the position denoted by a specific sequence number.
    # TRIM_HORIZON - Start reading at the last untrimmed record in the shard in the system, which is the oldest data record in the shard.
    # LATEST - Start reading just after the most recent record in the shard, so that you always read the most recent data in the shard.
    shard_id = None

    # Private
    _shard_it = None

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

    def __init__(self, client, topic, mode, num_procs=1, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchChannelKinesis, self).__init__(client, topic, mode, num_procs=num_procs)
        self.shard_it_type = shard_it_type
        self.shard_id = shard_id
        if mode == "duplex" or mode == "consumer":
            # Special Note:
            # GetShardIterator has a limit of 5 transactions per second per account per open shard.
            # http://boto3.readthedocs.org/en/latest/reference/services/kinesis.html#Kinesis.Client.get_shard_iterator
            response = self._client._client.get_shard_iterator(
                StreamName=(self._client.topic_prefix + self.topic),
                ShardId=self.shard_id,
                ShardIteratorType=self.shard_it_type)
            self._shard_it = response['ShardIterator']
        else:
            self._shard_it = None
