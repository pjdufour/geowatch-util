"""
node.py includes the base GeoWatchNode class
"""
from geowatchutil.codec.factory import build_codec


class GeoWatchNode(object):
    """
    GeoWatchNode is the base class for producers and consumers

    """

    # Public
    topic = None
    """
        A string field that represents the topic.  In GeoWatch, ``topic`` represents an Apache Kafka topic, AWS Kinesis stream, AWS SNS topic, or any consumer/producer backend's topic.
    """

    mode = None
    """
        A string field that represents the mode.  Either: ``duplex``, ``consumer``, or ``producer``.
    """

    # Private
    _client = None
    _codec = None
    _channel = None

    def delete_topic(self, timeout=5, verbose=False):
        return self._client.delete_topic(self.topic, timeout=timeout, verbose=verbose)

    def __init__(self, client, mode, codec, topic):
        """
        """
        self._client = client
        self.mode = mode
        self.topic = topic

        # Codec
        self._codec = build_codec(codec, channel=self._client.backend, templates=self._client.templates)

        # Channel
        # Set by consumer/producer after GeoWatchNode.__init__
        self._channel = None
