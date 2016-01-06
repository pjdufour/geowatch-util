GeoWatch Util / Getting Started!
================

Welcome to the documentation for GeoWatch Util, the engine of GeoWatch_.  To install, follow the `installation`_ instructions.

.. _geowatch: http://geowatch.io
.. _installation: installation.html


What is GeoWatch?
-----------------

GeoWatch is a spatially-enabled distributed message broker.  GeoWatch includes a suite of libraries that streamline information flow across a heterogeneous set streaming and batch data sources.

The primary requirement of GeoWatch is to connect streaming GeoJSON_ services and traditional batch processing GIS system, and vice versa.

.. _geojson: http://geojson.org/

What does it do?
----------------

GeoWatch provies an abstraction layer on top of a heterogenous set of streaming and batch data sources.  With a commonm API, GeoWatch is able to pass messages between streaming systems, buffer streaming messages for batch processing, send notifications, and generally enable system-to-system spatially-enabled communication.

What does it support?
---------------------

GeoWatch supports multple channels and stores, including the following:

**Streaming Channels**

1.  Apache Kafka - http://kafka.apache.org
2.  AWS Kinesis - https://aws.amazon.com/kinesis/
3.  AWS SNS - https://aws.amazon.com/sns/
4.  AWS SQS - https://aws.amazon.com/sqs/
5.  Slack - https://slack.com

**Batch Stores**

1.  Memcached - http://memcached.org/
2.  WFS - https://en.wikipedia.org/wiki/Web_Feature_Service
3.  AWS S3 - https://aws.amazon.com/s3/
4.  File

If using Django, consider using geowatch-django, too.  GeoWatch Django provides a consistent way to provision geowatch objects based on Django settings.  Therefore, you don't need to create your own settings.

Below is a list of simple patterns for provisioning consumers, producers, and stores by using the functions in `runtime.py` (:mod:`geowatchutil.runtime`).  More complex provisioing routines can be executed by directly calling the respective factory.py functions `build_client`, `build_consumer`, `build_producer`, and `build_stores`.

.. note::

    Multiple `examples`_ of GeoWatch in action are includec in the documentation.  These examples provide brokers for multiple examples.

    .. _examples: examples.html

.. note::

    Read a more in-depth explanation of the `API`_.

    .. _api: api.html
 
Or skip directly to the source code documenation.  Most public API functions are contained in :mod:`geowatchutil.runtime`.

How does it work?
------------

GeoWatch is built on top of the following key concepts: consumers, producers, stores, brokers, codecs, and mappings.

**Consumers**

Consumers retrieve and decode messages from an external channel, such as AWS Kinesis.  GeoWatch can then send those messages into another streaming channel using producers or into persistent storage using stores.

Currently supported channels include: `Apache Kafka`_, AWS Kinesis, and AWS SQS.

.. _Apache Kafka: http://kafka.apache.org/

Consumers user the runtime method provision_consumer.

**Producers**

Producers generate messages.  GeoWatch has a variety of codec for messages, such as plain text, list/tab-separated-values, json/dict, GeoJSON, etc.  Producer's will add messages to a remote channel, which could be a real "streaming" service such as AWS kinesis or a "one-way" channel such as Slack notifications.

Currently supported channels include: Apache Kafka, AWS Kinesis, AWS SQS, AWS SNS, and Slack.

Producers user the runtime method provision_producer.

**Stores**

Stores are used for persistant non-streaming storage of messages.  They can include file, document, or memory storage.  For example, dumping all message traffic to an AWS S3 object for long-term storage.  Or buffering the latest batch of messages in memcached for analysis across a multi-tenant infrastructure.

Stores use the runtime method provision_store.

**Brokers**

Brokers provide an object-oriented way of managing the flow of messages.  You can attach message consumers, message producers, and message stores to brokers.

Additionally, the GeoWatchBroker class can be extended to inject arbitray code directly into before/middle/after the message processing chain.  For example, extending GeoWatchBroker to set up a complex cron job that parses message data and adds to MongoDB.

**Codecs**

Codecs convert messages between external and internal data representations.  GeoWatch includes codecs for: plain text, JSON, GeoJSON, and WFS.

For example, for JSON, `encode` calls json.dumps(data) and `decode` calls json.loads(data).

**Mappings**

Mappings convert application-specific objects into dicts/json that are suitable for messaging.  Templates are channel-specific, while mappings are for generic use (application <----> geowatch).  Therefore, only the base class is in the geowatch-util library.

.. note::
    See GeoWatch in action on the examples_ page.

        .. _examples: examples.html
