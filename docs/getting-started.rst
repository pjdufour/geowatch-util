Getting Started!
================

First, install geowatch-util via pip.

If using Django, consider using geowatchdjango.


Stores
------

**File Store**

.. code-block:: python

    store_file = GeoWatchStoreFile(settings.STATS_REQUEST_FILE, "GeoWatchCodecJSON", which="first")

**S3 Store**

.. code-block:: python

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

.. code-block:: python

    broker = GeoWatchBroker(
        stores_out=stores_out,
        sleep_period=5,
        count=1,
        deduplicate=False,
        filter_last_one=False,
        timeout=5,
        verbose=True)
