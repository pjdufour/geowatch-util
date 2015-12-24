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
    client = kwargs.pop('client', None)
    codec = kwargs.pop('codec', None)
    topic = kwargs.pop('topic', None)
    topic_check = kwargs.get('topic_check', True)  # Defaults to True

    tries = 0
    while tries < max_tries:
        #try:
        if 1 == 1:
            if not client:
                from geowatchutil.client.factory import build_client
                client = build_client(backend, **kwargs)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic, verbose=verbose):
                        client.create_topic(topic)
                        try:
                            client.wait_topic(topic, verbose=verbose)
                        except:
                            print "Waited for topic.  Topic was never created."

                    if client.check_topic_exists(topic, verbose=verbose):
                        from geowatchutil.consumer.factory import build_consumer
                        consumer = build_consumer(client, codec, topic, **kwargs)

                else:
                    from geowatchutil.consumer.factory import build_consumer
                    consumer = build_consumer(client, codec, topic, **kwargs)


        #except:
        #    if verbose:
        #        print "Error in provision_consumer.  Could not get lock on GeoWatch server. Try "+str(tries)+"."
        #    client = None
        #    consumer = None

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
    topic_check = kwargs.get('topic_check', True)  # Defaults to True

    tries = 0
    while tries < max_tries:
        #try:
        if 1 == 1:
            if not client:
                from geowatchutil.client.factory import build_client
                client = build_client(backend, **kwargs)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic, verbose=verbose):
                        client.create_topic(topic)
                        try:
                            client.wait_topic(topic, verbose=verbose)
                        except:
                            print "Waited for topic.  Topic was never created."
                    
                    if client.check_topic_exists(topic, verbose=verbose):
                        from geowatchutil.producer.factory import build_producer
                        producer = build_producer(client, codec, topic)

                else:
                    from geowatchutil.producer.factory import build_producer
                    producer = build_producer(client, codec, topic)

        #except:
        #    if verbose:
        #        print "Error in provision_producer.  Could not get lock on GeoWatch server. Try "+str(tries)+"."
        #    client = None
        #    producer = None

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


def provision_brokers(watchlist, globalconfig=None, templates=None, actiontype=None, resourcetype=None, verbose=False):
    """
    Provision new GeoWatch brokers.

    ``watchlist`` is a list of broker dict configurations.

    ``globalconfig`` is a dict configuration for shared variables, such as AWS Region, AWS Credentials, etc.
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

    brokers = []
    for w in watchlist:
        if w['enabled']:
            if ((not actiontype) or (actiontype in w['action'])) and ((not resourcetype) or (resourcetype in w['resource'])):
                b = provision_broker(w, globalconfig=globalconfig, templates=templates, verbose=verbose)
                brokers.append(b)
    return brokers


def provision_broker(brokerconfig, globalconfig, templates=None, verbose=True):
    """
    Provision new GeoWatch broker.

    ``brokerconfig`` is a broker dict configurations.

    ``globalconfig`` is a dict configuration for shared variables, such as AWS Region, AWS Credentials, etc.
    Fallback for missing broker-specific values.

    :meth:`provision_broker` returns a :class:`GeoWatchBroker` broker.

    **Examples**

    .. code-block:: python

        from geowatchutil.runtime import provision_broker

        globalconfig = {'aws_access_key_id':'', 'aws_secret_access_key':'', 'aws_region':''}
        brokers = provision_brokers(settings.GEOWATCH_BROKERS_CRON, globalconfig=globalconfig)

        for broker in brokers:

            broker.run(maxcycle=1)

    """
    from geowatchutil.broker.factory import build_broker


    consumers = []
    producers = []
    stores_out = []

    if 'consumers' in brokerconfig:
        for c in brokerconfig['consumers']:
            if c['enabled']:
                c2 = copy.deepcopy(c)
                if globalconfig:
                    c2.update(globalconfig)
                consumers.extend(_build_geowatch_consumers(c2, verbose=verbose))

    if 'producers' in brokerconfig:
        for c in brokerconfig['producers']:
            if c['enabled']:
                c2 = copy.deepcopy(c)
                if globalconfig:
                    c2.update(globalconfig)
                producers.extend(_build_geowatch_producers(c2, templates=templates, verbose=verbose))

    if 'stores_out' in brokerconfig:
        for c in brokerconfig['stores_out']:
            if c['enabled']:
                c2 = copy.deepcopy(c)
                if globalconfig:
                    c2.update(globalconfig)
                store = provision_store(
                    c2['backend'],
                    c2['key'],
                    c2['codec'],
                    ** c2['options'])
                stores_out.append(store)

    broker = build_broker(
        brokerconfig['name'],
        brokerconfig['description'],
        count=brokerconfig.get('count', 1),
        consumers=consumers,
        producers=producers,
        stores_out=stores_out,
        deduplicate=False,
        verbose=verbose)

    return broker


def _build_geowatch_consumers(c, verbose=False):
    """
    Builds and returns list of consumers based on config `c`.
    """
    consumers = []
    topics = c['topics'] if ('topics' in c) else ([c['topic']] if ('topic' in c) else [])
    client = None
    for topic in topics:
        client, consumer = provision_consumer(
            c['backend'],
            topic=topic,
            topic_check=c.get('topic_check', None),
            client=client,
            codec=c['codec'],
            topic_prefix=c.get('topic_prefix', None),
            aws_region=c.get('aws_region', None),
            aws_access_key_id=c.get('aws_access_key_id', None),
            aws_secret_access_key=c.get('aws_secret_access_key', None),
            verbose=verbose)
        consumers.append(consumer)
    return consumers


def _build_geowatch_producers(c, templates=None, verbose=False):
    """
    Builds and returns list of producers based on config `c`.
    """
    producers = []
    topics = c['topics'] if ('topics' in c) else ([c['topic']] if ('topic' in c) else [])
    client = None
    for topic in topics:
        client, producer = provision_producer(
            c['backend'],
            topic=topic,
            topic_check=c.get('topic_check', None),
            client=client,
            codec=c['codec'],
            templates=(getattr(templates, c['templates'], None) if ('templates' in c) else None),
            url_webhook=c.get('url_webhook', None),
            authtoken=c.get('authtoken', None),
            topic_prefix=c.get('topic_prefix', None),
            aws_region=c.get('aws_region', None),
            aws_access_key_id=c.get('aws_access_key_id', None),
            aws_secret_access_key=c.get('aws_secret_access_key', None),
            verbose=verbose)
        producers.append(producer)
    return producers
