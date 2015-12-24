GEOWATCH_BROKER_BUILTIN_1 = {
    "enabled": True,
    "name": "--(GeoJSON)--> Kinesis",
    "description": "This broker pushes geojson messages to an AWS Kinesis stream.",
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
    "name": "Kinesis --(GeoJSON)--> WFS",
    "description": "This broker receives incoming geojson from an AWS kinesis stream and writes to GeoNode layers using WFS-T.",
    "consumers":
    [
        {
            "enabled": True,
            "backend": "kinesis",
            "codec": "json",
            "topic_prefix": "",
            "topic": "geowatch"
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
