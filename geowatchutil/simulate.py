import datetime

from geowatchutil.gw_random import build_random_featurecollection


def simulate_messages_geojson(featuretype=None, count=2, now=None, verbose=None):
    if not now:
        now = datetime.datetime.now()

    messages = []
    for i in range(count):
        data = build_random_featurecollection(verbose=verbose)
        message = {
            u'metadata': {
                u'featuretype': unicode(featuretype),
                u'date': unicode(now.isoformat())
            },
            u'data': data
        }
        messages.append(message)
    return messages
