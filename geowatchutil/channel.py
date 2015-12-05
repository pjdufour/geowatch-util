from kafka import SimpleProducer, MultiProcessConsumer


class GeoWatchChannel(object):

    # Public
    backend = None
    mode = None
    num_procs = None

    # Private
    _client = None

    def __init__(self, client, mode, num_procs=1):
        self._client = client
        self.backend = self._client.backend
        self.mode = mode
        self.num_procs = num_procs


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


class GeoWatchChannelTopic(GeoWatchChannel):

    # Public
    topic = None

    def __init__(self, client, topic, mode, num_procs=1):
        super(GeoWatchChannelTopic, self).__init__(client, mode, num_procs=1)
        self.topic = topic


class GeoWatchChannelKafka(GeoWatchChannelTopic):

    # Public
    group = None

    # Private
    _consumer = None
    _producer = None

    @classmethod
    def encode(cls, message):
        return message.encode('utf-8')

    @classmethod
    def decode(cls, message):
        return message.decode('utf-8')

    def send_message(self, message):
        self._producer.send_messages(self.topic, message)

    def send_messages(self, messages):
        self._producer.send_messages(self.topic, *messages)

    def get_messages_raw(self, count, block=True, timeout=5):
        return self._consumer.get_messages(count=count, block=True, timeout=timeout)

    def __init__(self, client, topic, mode, num_procs=1, group=None):
        super(GeoWatchChannelKafka, self).__init__(client, topic, mode, num_procs=num_procs)
        self.group = group
        if mode == "duplex" or mode == "producer":
            self._producer = SimpleProducer(self._client._client)
        if mode == "duplex" or mode == "consumer":
            self._consumer = MultiProcessConsumer(self._client._client, self.group, self._client.topic_prefix + self.topic, num_procs=self.num_procs)


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
            records.append({'Data':message, 'PartitionKey':partition_key})
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
