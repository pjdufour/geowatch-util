"""
Provides runtime functions.  These functions wrap factory functions with exception handling and timeouts.
"""
import time


def provision_consumer(backend, **kwargs):
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
        #try:
        if 1 == 1:
            if not client:
                from geowatchutil.client.factory import build_client
                client = build_client(backend, **kwargs)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic):
                        client.create_topic(topic)


                from geowatchutil.producer.factory import build_producer
                consumer = build_consumer(client, codec, topic, **kwargs)


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


def provision_producer(backend, **kwargs):
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
        # try:
        if 1 == 1:
            if not client:
                from geowatchutil.client.factory import build_client
                client = build_client(backend, **kwargs)

            if client:
                if topic and topic_check:
                    if not client.check_topic_exists(topic):
                        client.create_topic(topic)

                from geowatchutil.producer.factory import build_producer
                producer = build_producer(client, codec, topic)

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


def provision_store(backend, key, codec, **kwargs):
    store = None

    verbose = kwargs.get('verbose', False)
    max_tries = kwargs.get('max_tries', 12)
    sleep_period = kwargs.get('sleep_period', 5)

    tries = 0
    while tries < max_tries:
        # try:
        if 1 == 1:
            from geowatchutil.store.factory import build_store
            store = build_store(backend, key, codec, **kwargs)

        #except:
        #    if verbose:
        #        print "Could not get lock on GeoWatch server. Try "+str(tries)+"."
        #    client = None
        #    producer = None

        if store:
            break

        tries += 1
        time.sleep(sleep_period)
    return store
