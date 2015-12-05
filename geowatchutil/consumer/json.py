from geowatchutil.consumer.base import GeoWatchConsumer

from geowatchutil.codec.json import GeoWatchCodecJSON

class GeoWatchConsumerJSON(GeoWatchConsumer):

    def __init__(self, client, topic, num_procs, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
        super(GeoWatchConsumerJSON, self).__init__(
            client,
            topic,
            GeoWatchCodecJSON(channel=client.backend),
            num_procs,
            group=group,
            shard_id=shard_id,
            shard_it_type=shard_it_type)
