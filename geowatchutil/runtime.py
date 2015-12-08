import time

from geowatchutil.client.factory import create_client_file, create_client_kafka, create_client_kinesis
from geowatchutil.consumer.factory import create_consumer_kafka, create_consumer_kinesis
from geowatchutil.factory import create_producer


def provision_consumer_file(path, client=None, codec="GeoWatchCodecPlain", topic_check=False, verbose=False):
    return _provision_consumer(
        "file",
        None,
        topic_check=topic_check,
        codec=codec,
        path=path,
        client=client,
        verbose=verbose
    )


def provision_consumer_kafka(host=None, client=None, topic=None, codec="GeoWatchCodecPlain", topic_prefix="", max_tries=12, timeout=5, sleep_period=5, topic_check=False, verbose=False):
    return _provision_consumer(
        "kafka",
        topic,
        topic_check=topic_check,
        codec=codec,
        host=host,
        client=client,
        topic_prefix=topic_prefix,
        max_tries=max_tries,
        timeout=timeout,
        sleep_period=sleep_period,
        verbose=verbose
    )


def provision_consumer_kinesis(topic=None, codec="GeoWatchCodecPlain", aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, shard_id='shardId-000000000000', shard_it_type="LATEST", client=None, topic_prefix="", max_tries=12, timeout=5, sleep_period=5, topic_check=False, verbose=False):
    return _provision_consumer(
        "kinesis",
        topic,
        topic_check=topic_check,
        codec=codec,
        client=client,
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        shard_id=shard_id,
        shard_it_type=shard_it_type,
        topic_prefix=topic_prefix,
        max_tries=max_tries,
        timeout=timeout,
        sleep_period=sleep_period,
        verbose=verbose
    )


def _provision_consumer(backend, topic, codec="GeoWatchCodecPlain", path=None, host=None, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, shard_id='shardId-000000000000', shard_it_type="LATEST", client=None, topic_prefix="", max_tries=12, timeout=5, sleep_period=5, topic_check=False, verbose=False):
    consumer = None
    tries = 0
    while tries < max_tries:
        #try:
        if 1==1:
            if not client:
                if backend == "file":
                    client = create_client_file(path)
                elif backend == "kafka":
                    client = create_client_kafka(host, topic_prefix)
                elif backend == "kinesis":
                    client = create_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic):
                        client.create_topic(topic)

                if backend == "kafka":
                    client, consumer = create_consumer_kafka(
                        topic,
                        codec=codec,
                        client=client,
                        num_procs=4)
                elif backend == "kinesis":
                    client, consumer = create_consumer_kinesis(
                        topic,
                        codec=codec,
                        client=client,
                        num_procs=4,
                        shard_id=shard_id,
                        shard_it_type=shard_it_type)

        #except:
        #        if verbose:
        #            print "Could not get lock on GeoWatch server. Try "+str(tries)+"."
        #        client = None
        #        consumer = None

        if consumer:
            break

        tries += 1
        time.sleep(sleep_period)
    return (client, consumer)


def provision_producer(backend, topic=None, codec="GeoWatchCodecPlain", path=None, host=None, aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, client=None, topic_prefix="", max_tries=12, timeout=5, sleep_period=5, topic_check=False, verbose=False):
    producer = None
    tries = 0
    while tries < max_tries:
        if 1==1:
        #try:
            if not client:
                if backend == "file":
                    client = create_client_file(path)
                elif backend == "kafka":
                    client = create_client_kafka(host, topic_prefix)
                elif backend == "kinesis":
                    client = create_client_kinesis(aws_region, aws_access_key_id, aws_secret_access_key, topic_prefix)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic):
                        client.create_topic(topic)

                client, producer = build_producer(backend, topic, codec=codec, client=client)

        #except:
        #    if verbose:
        #        print "Could not get lock on GeoWatch server. Try "+str(tries)+"."
        #    client = None
        #    producer = None

        if producer:
            break

        tries += 1
        time.sleep(sleep_period)
    return (client, producer)
