GEOWATCH_BROKER_BUILTIN_1 = {
    "enabled": True,
    "name": "--(GeoJSON)--> Kinesis",
    "description": "This broker pushes geojson messages to an AWS Kinesis stream.",
    "count": 2,  # maximum number of messages consumed per cycle
    "producers":
    [
        {
            "enabled": True,
            "backend": "kinesis",
            "codec": "geojson",
            "topic_prefix": "",
            "topic": "geowatch-geonode",
            "topic_check": True  # Create topic if does not exist
        }
    ]
}

GEOWATCH_BROKER_BUILTIN_2 = {
    "enabled": True,
    "name": "Kinesis --(GeoJSON)-->",
    "description": "This broker consumes geojson messages from an AWS Kinesis stream.",
    "count": 2,  # maximum number of messages consumed per cycle
    "consumers":
    [
        {
            "enabled": True,
            "backend": "kinesis",
            "codec": "geojson",
            "topic_prefix": "",
            "topic": "geowatch-geonode",
            "topic_check": True  # Create topic if does not exist
        }
    ]
}


GEOWATCH_BROKER_BUILTIN_3 = {
    "enabled": True,
    "name": "Kinesis --(GeoJSON)--> WFS",
    "description": "This broker receives incoming geojson from an AWS kinesis stream and writes to GeoNode layers using WFS-T.",
    "count": 2,
    "consumers":
    [
        {
            "enabled": True,
            "backend": "kinesis",
            "codec": "geojson",
            "topic_prefix": "",
            "topic": "geowatch-geonode",
            "topic_check": True  # Create topic if does not exist
        }
    ],
    "stores_out":
    [
        {
            "enabled": True,
            "backend": "wfs",
            "key": None,
            "codec": "wfs",
            "options": {
                "url": "http://localhost:8080/geoserver/wfs",
                "auth_user": "admin",
                "auth_password": "admin"
            }
        }
    ]
}
