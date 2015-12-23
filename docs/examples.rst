GeoWatch Util / Examples
========

Below are a list of standard examples, configured as dicts and as direct code.

You can download these examples_ and more on GitHub.

.. _examples: https://github.com/geowatch/geowatch-examples


AWS Kinesis to WFS
------------------

**local_settings.py**

.. code-block:: python

    GEOWATCH_BROKERS = [
        {
            "enabled": True,
            "name": "Kinesis to WFS",
            "description": "Incoming GeoJSON from AWS Kinesis to WFS",
            "consumers":
            [
                {
                    "enabled": True,
                    "backend": "kinesis",
                    "codec": "json",
                    "topic_prefix": "",
                    "topic": "geowatch-geonode"
                }
            ],
            "stores_out":
            [
                {
                    "enabled": True,
                    "backend": "wfs",
                    "key": None,
                    "codec": "wfs",
                    "options": {
                        "url": "http://localhost:8080/geoserver/wfs",
                        "auth_user": "admin",
                        "auth_password": "admin"
                    }
                }
            ]
        }
    ]

**geowatch-brokers.py**

.. code-block:: python

    from multiprocessing import Process, Lock, Queue, cpu_count

    from django.conf import settings

    from geowatch.runtime import provision_brokers


    def run(broker):
        broker.run()

    verbose = True
    brokers = provision_brokers(settings.GEOWATCH_BROKERS_CRON)

    if not brokers:
        print "Could not provision brokers."
    else:
        print str(cpu_count())+" CPUs are available."
        processes = []
        processID = 1
        for broker in brokers:
            process = Process(target=run,args=(broker,))
            process.start()
            processes.append(process)
            processID += 1

        print "Provisioned "+str(len(brokers))+" brokers."


Multiple Apache Kafka to AWS Kinesis
------------------------------------

.. code-block:: python

    GEOWATCH_BROKERS = [
        {
            "enabled": True,
            "name": "Logs",
            "description": "Aggregate incoming logs from multiple Apache topics to AWS Kinesis",
            "consumers":
            [
                {
                    "enabled": True,
                    "backend": "kafka",
                    "codec": "plain",
                    "topic": "logs-master",
                    "host": "localhost"
                },
                {
                    "enabled": True,
                    "backend": "kafka",
                    "codec": "plain",
                    "topic": "logs-worker",
                    "host": "localhost"
                }
            ],
            "producers":
            [
                {
                    "enabled": True,
                    "backend": "kinesis",
                    "codec": "wfs",
                    "topic": "logs-aggregate",
                    "aws_region"=XXX,
                    "aws_access_key_id"=XXX,
                    "aws_secret_access_key"=XXX
                }
            ]
        }
    ]



**Apache Kafka**

.. code-block:: python

    from geowatchutil.runtime import provision_consumer

    client, consumer = provision_consumer(
        "kafka",
        host=None,
        topic=None,
        codec="plain",
        topic_prefix="",
        max_tries=12,
        timeout=5,
        sleep_period=5,
        topic_check=False,
        verbose=False):

**AWS Kinesis**

.. code-block:: python

    from geowatchutil.runtime import provision_consumer_kafka

    client, consumer = provision_consumer(
        "kinesis",
        topic=None,
        codec="GeoWatchCodecPlain",
        aws_region=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        shard_id='shardId-000000000000',
        shard_it_type="LATEST",
        client=None,
        topic_prefix="",
        max_tries=12,
        timeout=5,
        sleep_period=5,
        topic_check=False,
        verbose=False):

.. code-block:: python

    from geowatchutil.runtime import provision_producer

    client, producer = provision_producer(
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

.. code-block:: python

    from geowatchutil.store.factory import provision_store

    store_file = provision_store(
        "file",
        settings.STATS_REQUEST_FILE,
        "json",
        which="first")

**S3 Store**

.. code-block:: python

    from geowatchutil.store.factory import provision_store

    store_s3 = provision_store(
        "s3"
        "final_stats.json",
        "json",
        aws_region=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_bucket="tilejet",
        which="first")

**Memcached Store**

.. code-block:: python

    from geowatchutil.store.factory import provision_store

    store_memcached = provision_store(
        "memcached",
        "stats.json",
        "json",
        client_type="umemcache",
        which="first",
        host="localhost",
        port=11211)

**WFS Store**

.. code-block:: python

    from geowatchutil.store.factory import provision_store

    store_wfs = provision_store(
        "wfs",
        key,
        "wfs",
        url="http://geonode.org/geoserver/geonode/wfs/"
        auth_user="admin",
        auth_password="admin")


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


Kinesis to WFS
--------------


..code:: python

    


Kafka to Slack
--------------
