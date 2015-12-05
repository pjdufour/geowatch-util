from geowatchutil.consumer.base import GeoWatchConsumer

from geowatchutil.codec.tilerequest import GeoWatchCodecTileRequest


class GeoWatchConsumerTileRequest(GeoWatchConsumer):

    def receive_tile_requests(self, count, ttl=60, block=True, timeout=5, now=None):
        now = assert_now(now)
        response = self.get_messages_raw(count, block=block, timeout=timeout)
        if self._client.backend == "kafka":
            return self._receive_tile_requests_kafka(response, now, ttl)
        elif self._client.backend == "kinesis":
            return self._receive_tile_requests_kinesis(response, now, ttl)

    def _receive_tile_requests_kafka(self, response, now, ttl):
        messages_decoded = []
        for item in response:
            offset, message = item
            message_decoded = self._codec.decode_channel(message.value)
            itempart = message_decoded.split(";")
            date = parse_date(itempart[0])
            if not date:
                print "Date is missing or invalid!"
            elif is_expired(date, now, ttl):
                # print "Tile expired!"
                continue
            else:
                messages_decoded.append(itempart[1])  # Covert to dict within client application

        return messages_decoded

    def _receive_tile_requests_kinesis(self, response, now, ttl):
        self._channel._shard_it = response[u'NextShardIterator']
        messages_decoded = []
        for item in response[u'Records']:
            # partition_key = item[u'PartitionKey']
            message = item[u'Data']
            message_decoded = self._codec.decode_channel(message)
            itempart = message_decoded.split(";")
            date = parse_date(itempart[0])
            if not date:
                print "Date is missing or invalid!"
            elif is_expired(date, now, ttl):
                # print "Tile expired!"
                continue
            else:
                messages_decoded.append(itempart[1])  # Covert to dict within client application

        return messages_decoded

    def __init__(self, client, topic, num_procs, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumerTileRequest, self).__init__(
            client,
            topic,
            GeoWatchCodecTileRequest(channel=client.backend),
            num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
