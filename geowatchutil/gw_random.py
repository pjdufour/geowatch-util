import random
import string

from geojson import Feature, FeatureCollection, Point


def build_random_properties(count=2):
    letters = string.ascii_lowercase
    p = {}
    for i in range(count):
        # j = random.randint(0, 25)
        j = letters[i]
        k = random.randint(0, 25)
        p[j] = letters[k]
    return p


def build_random_point(minx=-180.0, miny=-90.0, maxx=180.0, maxy=90.0):
    x = random.uniform(minx, maxx)
    y = random.uniform(miny, maxy)
    return Point((x,y))


def build_random_feature():
    p = build_random_properties(count=2)
    g = build_random_point()
    f = Feature(geometry=g, properties=p)
    return f


def build_random_featurecollection(verbose=None):
    features = []
    for i in range(2):
        if verbose:
            print "Building random feature ", i
        features.append(build_random_feature())
    fc = FeatureCollection(features)
    return fc
