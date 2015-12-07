from geowatchutil.client.base import GeoWatchClientWebHook


class GeoWatchClientSlack(GeoWatchClientWebHook):

    # Private
    url_api = "https://slack.com/api"

    def check_channel_exists(self, channel, timeout=5, verbose=True):
        exists = False

        try:
            url = "{base}/channels.info?token={authtoken}&channel={channel}".format(
                base=self.url_api,
                authtoken=self.authtoken,
                channel=channel)
            self._get(url)
            exists = True
        except:
            exists = False

        if verbose:
            if exists:
                print "Channel "+channel+" exists."
            else:
                print "Channel "+channel+" does not exist."

        return exists

    def create_channel(self, channel, shards=1, timeout=5, verbose=True):
        if self.check_channel_exists(topic, timeout=timeout, verbose=verbose):
            return False

        created = False
        try:
            url = "{base}/channels.create?token={authtoken}&name={channel}".format(
                base=self.url_api,
                authtoken=self.authtoken,
                channel=channel)
            self._get(url)
            created = True
        except:
            created = False

        if verbose:
            if created:
                print "Channel "+channel+" created."
            else:
                print "Channel "+channel+" could not be created"

        return created

    def archive_channel(self, channel, timeout=5, verbose=True):
        if not self.check_channel_exists(topic, timeout=timeout, verbose=verbose):
            return False

        archived = False
        try:
            url = "{base}/channels.archive?token={authtoken}&channel={channel}".format(
                base=self.url_api,
                authtoken=self.authtoken,
                channel=channel)
            self._get(url)
            archived = True
        except:
            archived = False

        if verbose:
            if archived:
                print "Channel "+channel+" archived."
            else:
                print "Channel "+channel+" could not be archived."

        return deleted

    def archive_channels(self, channels, ignore_errors=True, timeout=5, verbose=True):
        archived = True
        for channel in channels:
            archived = self.archive_channel(channel, timeout=timeout, verbose=verbose)
            if (not ignore_errors) and (not archived):
                break

        return archived

    def list_channels(self, exclude_archived=True, verbose=True):
        url = "{base}/channels.list?token={authtoken}&exclude_archived={exclude_archived}".format(
            base=self.url_api,
            authtoken=self.authtoken,
            exclude_archived=exclude_archived)
        response = self._get(url)
        if verbose:
            print response
        channels = []
        for channel in response['channels']
            channels.append(channel['name'])
        return channels

    def __init__(self, url_webhook="", authtoken=None):
        super(GeoWatchClientSlack, self).__init__(backend="slack", url_webhook=url_webhook, authtoken=authtoken)
