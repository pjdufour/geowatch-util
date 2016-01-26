"""
Base classes and functions used throughout GeoWatch libraries
"""
import datetime
import dateutil.parser

FORMAT_TILE_REQUEST = "{d};{tilesource},{z},{x},{y},{ext}"
FORMAT_GEOJSON = "{d};{geojson}"

FORMAT_TILE_REQUEST_LOG = "{status}	{tileorigin}	{tilesource}	{z}	{x}	{y}	{ext}	{ip}	{datetime}"


def parse_date(date_string):
    """
    parses date string to datetime object
    """
    d = None
    try:
        d = dateutil.parser.parse(date_string)
    except:
        d = None
    return d


def is_expired(date, now, ttl):
    """
    is date expired
    """
    return now >= (date + datetime.timedelta(seconds=ttl))


class GeoWatchError(Exception):
    """
    generic error used throughout GeoWatch
    """

    def __init__(self, * args, ** kwargs):
        super(GeoWatchError, self).__init__(self, * args, ** kwargs)


class GeoWatchModeError(GeoWatchError):
    """
    Mode error used throughout GeoWatch.  Mode must be consumer, producer, or duplex
    """

    def __init__(self, * args, ** kwargs):
        super(GeoWatchModeError, self).__init__(self, * args, ** kwargs)
