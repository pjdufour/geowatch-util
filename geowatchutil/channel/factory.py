def build_channel(channel, client=None, topic=None, mode=None, num_procs=1, group=None, shard_id=u'shardId-000000000000', shard_it_type='LATEST'):
    """
    build_channel returns a GeoWatchChannel object based on the given well-known name
    """
    channel_lc = channel.lower()
    if channel_lc == "file" or channel_lc == "geowatchchannelfile":
        from geowatchutil.channel.geowatch_channel_file import GeoWatchChannelFile
        return GeoWatchChannelFile(client, mode)
    elif channel_lc == "kafka" or channel_lc == "geowatchchannelkafka":
        from geowatchutil.channel.geowatch_channel_kafka import GeoWatchChannelKafka
        return GeoWatchChannelKafka(client, topic, mode, num_procs=num_procs, group=group)
    elif channel_lc == "kinesis" or channel_lc == "geowatchchannelkinesis":
        from geowatchutil.channel.geowatch_channel_kinesis import GeoWatchChannelKinesis
        return GeoWatchChannelKinesis(client, topic, mode, num_procs=num_procs, shard_id=shard_id, shard_it_type=shard_it_type)
    elif channel_lc == "sns" or channel_lc == "geowatchchannelsns":
        from geowatchutil.channel.geowatch_channel_sns import GeoWatchChannelSNS
        return GeoWatchChannelSNS(client, topic, mode)
    elif channel_lc == "sqs" or channel_lc == "geowatchchannelsqs":
        from geowatchutil.channel.geowatch_channel_sqs import GeoWatchChannelSQS
        return GeoWatchChannelSQS(client, topic, mode)
    elif channel_lc == "slack" or channel_lc == "geowatchchannelslack":
        from geowatchutil.channel.geowatch_channel_slack import GeoWatchChannelSlack
        return GeoWatchChannelSlack(client, topic, mode)
