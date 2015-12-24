import random
import string

from geojson import Feature, FeatureCollection, Point

def build_random_properties():
    letters = string.ascii_lowercase
    p = {}
    for i in range(4):
        # j = random.randint(0, 25)
        j = letters[i]
        k = random.randint(0, 25)
        p[j] = letters[k]
    return p


def build_random_point():
    x = random.uniform(-180.0, 180.0)
    y = random.uniform(-90.0, 90.0)
    return Point((x,y))


def build_random_feature():
    p = build_random_properties()
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
