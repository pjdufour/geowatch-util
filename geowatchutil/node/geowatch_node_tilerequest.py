from geowatchutil.base import parse_date, is_expired
from geowatchutil.node.base import GeoWatchNodeDuplex, assert_now


class GeoWatchNodeTileRequest(GeoWatchNodeDuplex):

    # Consumer Functions
    def get_messages(self, count, block=True, timeout=5, ttl=60, now=None):
        now = assert_now(now)
        response = self._get_messages_raw(count, block=block, timeout=timeout)
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

    # Producer Functions
    def send_tile_requests(self, tilesource, tiles, extension='png', now=None):
        now = assert_now(now)
        messages_encoded = self._codec.encode(tilesource=tilesource, tiles=tiles, extension=extension, now=now)
        return self.send_messages(messages_encoded)

    def __init__(self, client, mode, topic, num_procs=1, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchNodeTileRequest, self).__init__(
            client,
            mode,
            "tilerequest",
            topic,
            num_procs=num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
