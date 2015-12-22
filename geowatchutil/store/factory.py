def build_store(backend, key, codec, **kwargs):
    store = None
    if backend == "file":
        from geowatchutil.store.geowatch_store_file import GeoWatchStoreFile
        return GeoWatchStoreFile(key, codec, **kwargs)
    elif backend == "s3":
        from geowatchutil.store.geowatch_store_s3 import GeoWatchStoreS3
        return GeoWatchStoreS3(key, codec, **kwargs)
    #elif backend == "memcached"
    #    from geowatchutil.store.geowatch_store_memcached import GeoWatchStoreMemcached
    #    return GeoWatchStoreMemcached(key, codec, **kwargs)
    elif backend == "wfs":
        from geowatchutil.store.geowatch_store_wfs import GeoWatchStoreWFS
        return GeoWatchStoreWFS(key, codec, **kwargs)
    return store

