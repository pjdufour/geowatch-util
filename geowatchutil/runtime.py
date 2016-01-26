"""
Provides runtime functions.  These functions wrap factory functions with exception handling and timeouts.
"""
import copy
import time

from geowatchutil.base import GeoWatchError, GeoWatchModeError


def provision_consumer(backend, **kwargs):
    return provision_node(backend, "consumer", **kwargs)


def provision_producer(backend, **kwargs):
    return provision_node(backend, "producer", **kwargs)


def provision_duplex(backend, **kwargs):
    return provision_node(backend, "duplex", **kwargs)


def provision_node(backend, mode, **kwargs):
    """
    Provision a new GeoWatch Node.

    ``backend`` is either: 'kafka', 'kinesis', 'slack', 'sns', or 'sqs'.

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

    if mode not in ["consumer", "producer", "duplex"]:
        raise GeoWatchModeError("GeoWatch mode error in provision_node.")

    node = None

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
                        from geowatchutil.node.factory import build_node
                        node = build_node(client, node, codec, topic, **kwargs)

                else:
                    from geowatchutil.node.factory import build_node
                    node = build_node(client, node, codec, topic, **kwargs)

        if node:
            break

        tries += 1
        time.sleep(sleep_period)
    return (client, node)


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


def provision_brokers(watchlist, globalconfig=None, templates=None, brokerfilter=None, verbose=False):
    """
    Provision new GeoWatch brokers.


    ``watchlist`` is a list of broker dict configurations.
    ``globalconfig`` is a dict configuration for shared variables, such as AWS Region, AWS Credentials, etc.
    Fallback for missing broker-specific values.

    If ``brokerfilter`` are non-None then they are used for filtering the brokers against their message filters.
    This is more efficient than initializing brokers that will never be used.

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
        if w.get('enabled', True):
            valid = True
            if brokerfilter and ('filter_metadata' in w):
                for k in brokerfilter:
                    if not ((k in w['filter_metadata']) and (brokerfilter[k] in w['filter_metadata'][k])):
                        valid = False
                        break

            if valid:
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

    broker_kwargs = build_broker_kwargs(
        brokerconfig,
        globalconfig,
        templates=templates,
        verbose=verbose)

    broker = build_broker(
        brokerconfig.get('name', None),
        brokerconfig.get('description', None),
        **broker_kwargs)

    return broker


def build_broker_kwargs(brokerconfig, globalconfig, templates=None, verbose=False):
    consumers = []
    producers = []
    duplex = []
    stores_out = []

    if 'consumers' in brokerconfig:
        for c in brokerconfig['consumers']:
            if c.get('enabled', True):
                c2 = copy.deepcopy(c)
                if globalconfig:
                    c2.update(globalconfig)
                consumers.extend(_provision_geowatch_nodes("consumer", c2, verbose=verbose))

    if 'producers' in brokerconfig:
        for c in brokerconfig['producers']:
            if c.get('enabled', True):
                c2 = copy.deepcopy(c)
                if globalconfig:
                    c2.update(globalconfig)
                producers.extend(_provision_geowatch_nodes("producer", c2, templates=templates, verbose=verbose))

    if 'duplex' in brokerconfig:
        for c in brokerconfig['duplex']:
            if c.get('enabled', True):
                c2 = copy.deepcopy(c)
                if globalconfig:
                    c2.update(globalconfig)
                duplex.extend(_provision_geowatch_nodes("duplex", c2, templates=templates, verbose=verbose))

    if 'stores_out' in brokerconfig:
        for c in brokerconfig['stores_out']:
            if c.get('enabled', True):
                c2 = copy.deepcopy(c)
                if globalconfig:
                    c2.update(globalconfig)
                store = provision_store(
                    c2['backend'],
                    c2['key'],
                    c2['codec'],
                    ** c2['options'])
                stores_out.append(store)

    return {
        "filter_metadata": brokerconfig.get('filter_metadata', None),
        "count": brokerconfig.get('count', 1),
        "consumers": consumers,
        "producers": producers,
        "stores_out": stores_out,
        "deduplicate": False,
        "verbose": verbose
    }


def _provision_geowatch_nodes(mode, c, templates=None, verbose=False):
    """
    Builds and returns list of nodes based on config `c`.
    """
    nodes = []
    topics = c['topics'] if ('topics' in c) else ([c['topic']] if ('topic' in c) else [])
    client = None
    kwargs = {
        "topic": topic,
        "topic_check": c.get('topic_check', None),
        "client": client,
        "codec": c['codec'],
        "authtoken": c.get('authtoken', None),
        "topic_prefix": c.get('topic_prefix', None),
        "aws_region": c.get('aws_region', None),
        "aws_access_key_id": c.get('aws_access_key_id', None),
        "aws_secret_access_key": c.get('aws_secret_access_key', None),
        "verbose": verbose
    }

    if mode == "producer" or mode =="duplex":
        kwargs.update({
            "templates": (getattr(templates, c['templates'], None) if ('templates' in c) else None),
            "url_webhook": c.get('url_webhook', None)
        })

    for topic in topics:
        kwargs.update({'topic': topic})
        client, node = provision_node(c['backend'], mode, **kwargs)
        nodes.append(node)

    return nodes
