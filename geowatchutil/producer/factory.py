from geowatchutil.producer.base import GeoWatchProducer
from geowatchutil.producer.geowatch_producer_tilerequest import GeoWatchProducerTileRequest


def build_producer(client, codec, topic):
    producer = None
    codec_lc = codec.lower()
    if codec_lc == "tile_request" or codec_lc == "geowatchcodectilerequest":
        producer = GeoWatchProducerTileRequest(client, topic)
    else:
        producer = GeoWatchProducer(client, codec, topic)
    return producer
