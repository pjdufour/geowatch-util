from geowatchutil.producer.base import GeoWatchProdcer

from geowatchutil.codec.json import GeoWatchCodecJSON

class GeoWatchProducerJSON(GeoWatchProducer):

    def send_json(self, data, now=None):
        now = assert_now(now)
        message = self._codec.encode(data=data)
        return self.send_message(message)

    def __init__(self, client, topic):
        super(GeoWatchProducerJSON, self).__init__(client, topic, GeoWatchCodecJSON())
