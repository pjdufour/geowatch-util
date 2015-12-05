from geowatchutil.producer import GeoWatchProdcer

from geowatchutil.codec.plain import GeoWatchCodecPlain

class GeoWatchProducerPlain(GeoWatchProducer):

    def send_text(self, text, now=None):
        # now = assert_now(now)
        message = self._codec.encode(text=text)
        return self.send_message(message)

    def __init__(self, client, topic):
        super(GeoWatchProducerPlain, self).__init__(client, topic, GeoWatchCodecPlain())
