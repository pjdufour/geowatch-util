"""
Provides runtime functions.  These functions wrap factory functions with exception handling and timeouts.
"""
import copy
import time


def provision_consumer(backend, **kwargs):
    """
    Provision a new GeoWatch consumer.

    ``backend`` is either: 'kafka', 'kinesis', 'sns', or 'sqs'.

    If ``client=None`` in ``kwargs``, :meth:`provision_consumer` will create a client.

    :meth:`provision_consumer` returns a tuple ``(client, consumer)``.

    **Examples**

    .. code-block:: python

        from geowatchutil.runtime import provision_consumer

        client, consumer = provision_consumer('kafka', host="localhost")

        client, consumer = provision_consumer(
            'kinesis',
            aws_region=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            topic_prefix=topic_prefix)

    """
    consumer = None

    verbose = kwargs.get('verbose', False)
    max_tries = kwargs.get('max_tries', 12)
    sleep_period = kwargs.get('sleep_period', 5)
    client = kwargs.get('client', None)
    codec = kwargs.get('codec', None)
    topic = kwargs.get('topic', None)
    topic_check = kwargs.get('topic_check', False)

    tries = 0
    while tries < max_tries:
        try:
            if not client:
                from geowatchutil.client.factory import build_client
                client = build_client(backend, **kwargs)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic):
                        client.create_topic(topic)

                from geowatchutil.consumer.factory import build_consumer
                consumer = build_consumer(client, codec, topic, **kwargs)

        except:
            if verbose:
                print "Error in provision_consumer.  Could not get lock on GeoWatch server. Try "+str(tries)+"."
            client = None
            consumer = None

        if consumer:
            break

        tries += 1
        time.sleep(sleep_period)
    return (client, consumer)


def provision_producer(backend, **kwargs):
    """
    Provision a new GeoWatch Producer.

    ``backend`` is either: 'kafka', 'kinesis', 'sns', or 'sqs'.

    If ``client=None`` in ``kwargs``, :meth:`provision_producer` will create a client.

    :meth:`provision_producer` returns a tuple ``(client, producer)``.

    **Examples**

    .. code-block:: python

        from geowatchutil.runtime import provision_producer

        client, consumer = provision_producer('kafka', host="localhost")

        client, consumer = provision_producer(
            'kinesis',
            aws_region=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            topic_prefix=topic_prefix)

    """

    producer = None

    verbose = kwargs.get('verbose', False)
    max_tries = kwargs.get('max_tries', 12)
    sleep_period = kwargs.get('sleep_period', 5)
    client = kwargs.get('client', None)
    codec = kwargs.get('codec', None)
    topic = kwargs.get('topic', None)
    topic_check = kwargs.get('topic_check', False)

    tries = 0
    while tries < max_tries:
        try:
            if not client:
                from geowatchutil.client.factory import build_client
                client = build_client(backend, **kwargs)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic):
                        client.create_topic(topic)

                from geowatchutil.producer.factory import build_producer
                producer = build_producer(client, codec, topic)

        except:
            if verbose:
                print "Error in provision_producer.  Could not get lock on GeoWatch server. Try "+str(tries)+"."
            client = None
            producer = None

        if producer:
            break

        tries += 1
        time.sleep(sleep_period)
    return (client, producer)


def provision_store(backend, key, codec, **kwargs):
    """
    Provision a new GeoWatch store.

    ``backend`` is either: 'file', 'memcached', 's3', or 'wfs'.

    ``codec`` is either: 'plain', 'json', 'tilerequest', or 'wfs'.

    :meth:`provision_store` returns a ``store``.

    **Examples**

    .. code-block:: python

        from geowatchutil.runtime import provision_store

        store = provision_store(
            's3',
            'results.json',
            'json',
            aws_region=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_bucket=aws_bucket)

    """

    store = None

    verbose = kwargs.get('verbose', False)
    max_tries = kwargs.get('max_tries', 12)
    sleep_period = kwargs.get('sleep_period', 5)

    tries = 0
    while tries < max_tries:
        try:
            from geowatchutil.store.factory import build_store
            store = build_store(backend, key, codec, **kwargs)

        except:
            if verbose:
                print "Error in provision_store.  Could not get lock on GeoWatch server. Try "+str(tries)+"."
            store = None

        if store:
            break

        tries += 1
        time.sleep(sleep_period)
    return store


def provision_brokers(watchlist, config=None, templates=None, actiontype=None, resourcetype=None):
    """
    Provision new GeoWatch brokers.

    ``watchlist`` is a list of broker dict configurations.

    ``config`` is a dict configuration for shared variables, such as AWS Region, AWS Credentials, etc.
    Fallback for missing broker-specific values.

    If ``actiontype`` or resourcetype are non-None then they are used for filtering.

    :meth:`provision_brokers` returns a list of :class:`GeoWatchBroker` brokers.

    **Examples**

    .. code-block:: python

        from geowatchutil.runtime import provision_brokers

        config = {'aws_access_key_id':'', 'aws_secret_access_key':'', 'aws_region':''}
        brokers = provision_brokers(settings.GEOWATCH_BROKERS_CRON, config=config)

        for broker in brokers:

            broker.run(maxcycle=1)

    """

    from geowatchutil.broker.factory import build_broker

    brokers = []
    for w in watchlist:
        if w['enabled']:
            if ((not actiontype) or (actiontype in w['action'])) and ((not resourcetype) or (resourcetype in w['resource'])):
                producers = []
                stores_out = []
                if 'producers' in w:
                    for c in w['producers']:
                        if c['enabled']:
                            c2 = copy.deepcopy(c)
                            if config:
                                c2.update(config)
                            producers.extend(_build_geowatch_producers(c2, templates=templates))

                if 'stores_out' in w:
                    for c in w['stores_out']:
                        if c['enabled']:
                            c2 = copy.deepcopy(c)
                            c2.update(config)
                            store = provision_store(
                                c2['backend'],
                                c2['key'],
                                c2['codec'],
                                ** c2['options'])
                            stores_out.append(store)

                b = build_broker(
                    w['name'],
                    w['description'],
                    producers=producers,
                    stores_out=stores_out,
                    deduplicate=False,
                    verbose=True)
                brokers.append(b)

    return brokers


def _build_geowatch_producers(c, templates=None):
    """
    Builds and returns list of producers based on config `c`.
    """
    producers = []
    topics = c['topics'] if ('topics' in c) else ([c['topic']] if ('topic' in c) else [])
    client = None
    for topic in topics:
        client, p = provision_producer(
            c['backend'],
            topic=topic,
            client=client,
            codec=c['codec'],
            templates=(getattr(templates, c['templates'], None) if ('templates' in c) else None),
            url_webhook=c.get('url_webhook', None),
            authtoken=c.get('authtoken', None),
            topic_prefix=c.get('topic_prefix', None),
            aws_region=c.get('aws_region', None),
            aws_access_key_id=c.get('aws_access_key_id', None),
            aws_secret_access_key=c.get('aws_secret_access_key', None))
        producers.append(p)
    return producers
