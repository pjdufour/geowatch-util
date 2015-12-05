from geowatchutil.client import GeoWatchClient


class GeoWatchClientFile(GeoWatchClient):

    # Public
    path = ""

    def __init__(self, path=""):
        super(GeoWatchClientFile, self).__init__(backend="file")
        self.path = path
