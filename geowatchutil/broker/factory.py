from geowatchutil.broker.base import GeoWatchBroker

def build_broker(name, description, **kwargs):

    consumers = kwargs.get('consumers', None)
    producers = kwargs.get('producers', None)
    stores_in = kwargs.get('stores_in', None)
    stores_out = kwargs.get('stores_out', None)

    count = kwargs.get('count', 1)
    timeout = kwargs.get('timeout', 5)
    threads = kwargs.get('threads', 1)
    sleep_period = kwargs.get('sleep_period', 5)
    deduplicate = kwargs.get('deduplicate', False)
    filter_last_one = kwargs.get('filter_last_one', False)

    broker = GeoWatchBroker(
        name,
        description,
        consumers=consumers,
        producers=producers,
        stores_in=stores_in,
        stores_out=stores_out,
        count=count,
        timeout=timeout,
        threads=threads,
        sleep_period=sleep_period,
        deduplicate=deduplicate,
        filter_last_one=filter_last_one,
        verbose=verbose)

     return broker

