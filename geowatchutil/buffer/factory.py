from geowatchutil.buffer.base import GeoWatchBufferLocalMemory, GeoWatchBufferMongoDB

def build_buffer(**kwargs):
    """
    build_buffer returns a GeoWatchClient.  build_client is used by runtime.py.  For individual use cases, directly calling the subordinate functions such as build_client_kafka might make sense.
    """
    b = None

    limit = kwargs.pop('limit_outgoing', None)
    buffer_type = kwargs.pop('buffer_type', None)
    buffer_db_host = kwargs.pop('buffer_db_host', 'localhost')
    buffer_db_port = kwargs.pop('buffer_db_port', 27017)
    buffer_db_name = kwargs.pop('buffer_db_name', None)
    buffer_db_collection = kwargs.pop('buffer_db_collection', None)

    if buffer_type.lower() == "mongodb":
        b = GeoWatchBufferMongoDB(
            limit=limit,
            host=buffer_db_host,
            port=buffer_db_port,
            name=buffer_db_name,
            collection=buffer_db_collection)
    else:
        b = GeoWatchBufferLocalMemory(limit=limit)

    return b
