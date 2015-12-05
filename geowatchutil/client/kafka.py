from geowatchutil.client.base import GeoWatchClientTopic

from kafka import KafkaClient


class GeoWatchClientKafka(GeoWatchClientTopic):

    def check_topic_exists(self, topic, timeout=5, verbose=True):
        exists = False

        try:
            md = self._client.has_metadata_for_topic(self.topic_prefix + topic)
            exists = (md is not None)
        except:
            exists = False

        if verbose:
            if exists:
                print "Topic "+topic+" exists."
            else:
                print "Topic "+topic+" does not exist."

        return exists

    def create_topic(self, topic, shards=1, timeout=5, verbose=True):
        if self.check_topic_exists(topic, timeout=timeout, verbose=verbose):
            return False

        created = False
        try:
            self._client.ensure_topic_exists(self.topic_prefix + topic, timeout=timeout)
            created = True
        except:
            created = False

        if verbose:
            if created:
                print "Topic created."
            else:
                print "Topic could not be created"

        return created

    def delete_topic(self, topic, timeout=5, verbose=True):
        return False  # kafka client cannot delete topics.  Only server can.

    def delete_topics(self, topics, ignore_errors=True, timeout=5, verbose=True):
        return False  # kafka client cannot delete topics.  Only server can.

    def list_topics(self, limit=100, verbose=True):
        return self._client.topic_partitions.keys()

    def __init__(self, topic_prefix="", host=None):
        super(GeoWatchClientKafka, self).__init__(backend="kafka", topic_prefix=topic_prefix)

        if host:
            self._client = KafkaClient(host)
        else:
            print "Could not create GeoWatch client for kafka backend.  Missing parameters."
