import datetime
import dateutil.parser

FORMAT_TILE_REQUEST = "{d};{tilesource},{z},{x},{y},{ext}"
FORMAT_GEOJSON = "{d};{geojson}"

FORMAT_TILE_REQUEST_LOG = "{status}	{tileorigin}	{tilesource}	{z}	{x}	{y}	{ext}	{ip}	{datetime}"


def parse_date(date_string):
    d = None
    try:
        d = dateutil.parser.parse(date_string)
    except:
        d = None
    return d


def is_expired(date, now, ttl):
    return now >= (date + datetime.timedelta(seconds=ttl))
