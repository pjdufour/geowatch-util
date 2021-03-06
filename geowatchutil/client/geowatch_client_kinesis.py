from geowatchutil.client.base import GeoWatchClientTopic

import boto3


class GeoWatchClientKinesis(GeoWatchClientTopic):

    def check_topic_exists(self, topic, timeout=5, verbose=True):
        exists = False

        try:
            self._client.describe_stream(StreamName=(self.topic_prefix + topic))
            exists = True
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
            self._client.create_stream(StreamName=(self.topic_prefix + topic), ShardCount=shards)
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
        if not self.check_topic_exists(topic, timeout=timeout, verbose=verbose):
            return False

        deleted = False
        try:
            self._client.delete_stream(StreamName=(self.topic_prefix + topic))
            deleted = True
        except:
            deleted = False

        if verbose:
            if deleted:
                print "Topic "+topic+" deleted."
            else:
                print "Topic "+topic+" could not be deleted"

        return deleted

    def delete_topics(self, topics, ignore_errors=True, timeout=5, verbose=True):
        deleted = True
        for topic in topics:
            deleted = self.delete_topic(topic, timeout=timeout, verbose=verbose)
            if (not ignore_errors) and (not deleted):
                break

        return deleted

    def list_topics(self, limit=100, verbose=True):
        streams = self._client.list_streams(Limit=limit)
        stream_names = streams[u'StreamNames']
        return stream_names

    def wait_topic(self, topic, verbose=False):
        if verbose:
            print "Waiting for topic ", topic
        waiter = self._client.get_waiter('stream_exists')
        waiter.wait(StreamName=(self.topic_prefix + topic))

    def __init__(self, topic_prefix="", aws_region=None, aws_access_key_id=None, aws_secret_access_key=None):
        super(GeoWatchClientKinesis, self).__init__(backend="kinesis", topic_prefix=topic_prefix)

        if aws_region and aws_access_key_id and aws_secret_access_key:
            session = boto3.session.Session(
                region_name=aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
            self._client = session.client('kinesis')
        else:
            print "Could not create GeoWatch client for Kinesis Backend.  Missing parameters."
