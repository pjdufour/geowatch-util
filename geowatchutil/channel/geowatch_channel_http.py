from geowatchutil.channel.base import GeoWatchChannelTopic


class GeoWatchChannelHTTP(GeoWatchChannelTopic):

    # Public
    it_type = 'LATEST'
    # AT_SEQUENCE_NUMBER - Start reading exactly from the position denoted by a specific sequence number.
    # AFTER_SEQUENCE_NUMBER - Start reading right after the position denoted by a specific sequence number.
    # TRIM_HORIZON - Start reading at the last untrimmed record in the shard in the system, which is the oldest data record in the shard.
    # LATEST - Start reading just after the most recent record in the shard, so that you always read the most recent data in the shard.

    # Private
    _it_id = None

    @classmethod
    def encode(self, message):
        return message

    @classmethod
    def decode(self, message):
        return message

    def send_message(self, message):
      raise NotImplementedError

    def send_messages(self, messages):
        raise NotImplementedError

    def get_max_it_id(self, ignore_errors=True):
        max_it_id = -1

        request = self._client._make_request(
            url=self._client.url_max,
            contentType="text/plain")

        if request.getcode() != 200:
            if not ignore_errors:
                raise Exception("Could not get augmented diff status.")

        response = request.read()

        try:
            max_it_id = int(response)
        except:
            if not ignore_errors:
                raise Exception("Could not parse augmented diff status.")

        return max_it_id;

    def get_messages_raw(self, count, block=True, timeout=5):
        """
        get_messages_raw will return raw Kinesis objects
        """
        #return self._client._client.get_records(ShardIterator=self._shard_it, Limit=count)
        messages_raw = []

        max_it_id = self.get_max_it_id(ignore_errors=False)
        if self._it_id < max_it_id:
            for i in range(self._it_id, min(max_it_id+1, self._it_id + count)):
                request = self._client._make_request(params={'id': i, 'debug':'yes'}, contentType="text/xml")
                if request.getcode() != 200:
                    raise Exception("Could not get augmented diff.")
                response = request.read()
                messages_raw.append(response)
                self._it_id = i + 1

        return messages_raw

    def __init__(self, client, topic, mode, num_procs=1, it_type='LATEST', it_id=0):
        super(GeoWatchChannelHTTP, self).__init__(client, topic, mode, num_procs=num_procs)
        self.it_type = it_type
        if mode == "duplex" or mode == "consumer":
            if it_type == "LATEST":
                self._it_id = self.get_max_it_id(ignore_errors=False)
            elif it_type == "TRIM_HORIZON":
                self._it_id = 0
            elif it_type == "AT_SEQUENCE_NUMBER":
                self._it_id = it_id
            elif it_type == "AFTER_SEQUENCE_NUMBER":
                self._it_id = it_id + 1
        else:
            self._it_id = 0
