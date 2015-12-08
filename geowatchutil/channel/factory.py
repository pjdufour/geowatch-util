from geowatchutil.channel.geowatch_channel_file import GeoWatchChannelFile
from geowatchutil.channel.geowatch_channel_kafka import GeoWatchChannelKafka
from geowatchutil.channel.geowatch_channel_kinesis import GeoWatchChannelKinesis
from geowatchutil.channel.geowatch_channel_sns import GeoWatchChannelSNS
from geowatchutil.channel.geowatch_channel_sqs import GeoWatchChannelSQS
from geowatchutil.channel.geowatch_channel_slack import GeoWatchChannelSlack


def build_channel(channel, client=None, topic=None, mode=None, num_procs=1, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
    """
    build_channel returns a GeoWatchChannel object based on the given well-known name
    """
    channel_lc = channel_lc.lower()
    if channel_lc == "file" or channel_lc == "geowatchchannelfile":
        return GeoWatchChannelFile(client, mode)
    elif channel_lc == "kafka" or channel_lc == "geowatchchannelkafka":
        return GeoWatchChannelKafka(client, topic, mode, num_procs=num_procs, group=group)
    elif channel_lc == "kinesis" or channel_lc == "geowatchchannelkinesis":
        return GeoWatchChannelKinesis(client, topic, mode, num_procs=num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
    elif channel_lc == "sns" or channel_lc == "geowatchchannelsns":
        return GeoWatchChannelSNS(client, topic, mode)
    elif channel_lc == "sns" or channel_lc == "geowatchchannelsqs":
        return GeoWatchChannelSQS(client, topic, mode)
    elif channel_lc == "slack" or channel_lc == "geowatchchannelslack":
        return GeoWatchChannelSlack(client, topic, mode)
