Getting Started!
================

First, install geowatch-util via pip.

If using Django, consider using geowatch-django, too.  GeoWatch Django provides a consistent way to provision geowatch objects based on Django settings.  Therefore, you don't need to create your own settings.


Consumers
---------

Consumers retrieve and decode messages from an external channel, such as AWS Kinesis.  GeoWatch can then send those messages into another streaming channel using producers or into persistent storage using stores.

Currently supported channels include: Apache Kafka, AWS Kinesis, and AWS SQS.

.. code-block:: python

    from geowatchutil.runtime import provision_consumer_kafka

    provision_consumer_kafka(host=None, client=None, topic=None, codec="GeoWatchCodecPlain", topic_prefix="", max_tries=12, timeout=5, sleep_period=5, topic_check=False, verbose=False):


.. code-block:: python

    from geowatchutil.runtime import provision_consumer_kafka

    provision_consumer_kinesis(topic=None, codec="GeoWatchCodecPlain", aws_region=None, aws_access_key_id=None, aws_secret_access_key=None, shard_id='shardId-000000000000', shard_it_type="LATEST", client=None, topic_prefix="", max_tries=12, timeout=5, sleep_period=5, topic_check=False, verbose=False):


Producers
---------

Producers generate messages.  GeoWatch has a variety of codec for messages, such as plain text, list/tab-separated-values, json/dict, GeoJSON, etc.  Producer's will add messages to a remote channel, which could be a real "streaming" service such as AWS kinesis or a "one-way" channel such as Slack notifications.

Currently supported channels include: Apache Kafka, AWS Kinesis, AWS SQS, AWS SNS, and Slack.

.. code-block:: python

    from geowatchutil.runtime import provision_producer

    provision_producer(
        backend,
        topic=None,
        codec="GeoWatchCodecPlain",
        path=None,
        host=None,
        aws_region=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        client=None,
        topic_prefix="",
        max_tries=12,
        timeout=5,
        sleep_period=5,
        topic_check=False,
        verbose=False)

Stores
------

Stores are used for persistant non-streaming storage of messages.  They can include file, document, or memory storage.  For example, dumping all message traffic to an AWS S3 object for long-term storage.  Or buffering the latest batch of messages in memcached for analysis across a multi-tenant infrastructure.

**File Store**

.. code-block:: python

    from geowatchutil.store.geowatch_store_file import GeoWatchStoreFile

    store_file = GeoWatchStoreFile(settings.STATS_REQUEST_FILE, "GeoWatchCodecJSON", which="first")

**S3 Store**

.. code-block:: python

    from geowatchutil.store.geowatch_store_s3 import GeoWatchStoreS3

    store_s3 = GeoWatchStoreS3(
        "final_stats.json",
        "GeoWatchCodecJSON",
        aws_region=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_bucket="tilejet",
        which="first")

**Memcached Store**

.. code-block:: python

    from geowatchutil.store.geowatch_store_memcached import GeoWatchStoreMemcached

    store_memcached = GeoWatchStoreMemcached(
        "stats_tilerequests",
        "GeoWatchCodecJSON",
        client_type="umemcache",
        which="first",
        host="localhost",
        port=11211)

    stores_out = [store_file, store_s3, store_memcached]

Brokers
-------

Brokers provide an object-oriented way of managing the flow of messages.  You can attach message consumers, message producers, and message stores to brokers.

Additionally, the GeoWatchBroker class can be extended to inject arbitray code directly into before/middle/after the message processing chain.  For example, extending GeoWatchBroker to set up a complex cron job that parses message data and adds to MongoDB.

.. code-block:: python

    from geowatchutil.broker.base import GeoWatchBroker

    broker = GeoWatchBroker(
        stores_out=stores_out,
        sleep_period=5,
        count=1,
        deduplicate=False,
        filter_last_one=False,
        timeout=5,
        verbose=True)

    broker.run(max_cycle=1)  # loop once
    
    broker.run()  # infinite loop
