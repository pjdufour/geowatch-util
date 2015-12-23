GeoWatch Util / API
===================

The source code for :mod:`geowatchutil` is broken out into runtime_, factory_, and class functions.

.. runtime:

.. factory:

See below for a quick explanation.

Runtime
------

Most public API functions are contained in :mod:`geowatchutil.runtime`.  Runtime functions wrap broker, consumer, producer, and store functions with exception handling and multiple tries.

In most use cases, you should use :mod:`geowatchutil.runtime` rather than factory functions and certainly more than directly initializing a class.

.. note::

    Unless for custom subclasses, you can describe your information flow as dicts, so that you only ever need to call :func:`geowatchutil.runtime.provision_brokers`.

**Functions**

The 4 main runtime functions are:

1.  :func:`geowatchutil.runtime.provision_brokers`
2.  :func:`geowatchutil.runtime.provision_consumer`
3.  :func:`geowatchutil.runtime.provision_producer`
4.  :func:`geowatchutil.runtime.provision_store`

Factory
-------

Factory functions provide a single entry point for creating a broker, consumer, and producer, store, and codec, respectively.

**Functions**

The 5 main factory functions are:

1.  :func:`geowatchutil.broker.factory.build_broker`
2.  :func:`geowatchutil.consumer.factory.build_consumer`
3.  :func:`geowatchutil.producer.factory.build_producer`
4.  :func:`geowatchutil.store.factory.build_store`
5.  :func:`geowatchutil.codec.factory.build_codec`

**Modules**

View all modules @ `code`_.

.. _code: source-code/modules/modules.html

.. note::
    See GeoWatch in action on the examples_ page.

        .. _examples: examples.html

