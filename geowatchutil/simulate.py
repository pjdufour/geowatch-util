import datetime
import string

from geowatchutil.gw_random import build_random_featurecollection


def simulate_messages_geojson(featuretype=None, count=5, now=None, verbose=None):
    if not now:
        now = datetime.datetime.now()

    messages = []
    for i in range(count):
        data = build_random_featurecollection(verbose=verbose)
        message = {
            'metadata': {
                'featuretype': featuretype,
                'date': now.isoformat()
            },
            'data': data
        }
        messages.append(message)
    return messages
