import requests
import zipfile
import shapefile
import json


def get_file(url, filename):
    # url = 'http://download.geofabrik.de/europe/norway-latest.shp.zip'

    with open('/tmp/' + filename, 'wb') as handle:
        response = requests.get(url, stream=True)

        for block in response.iter_content(1024):
            handle.write(block)


def unzip(filename):
    with zipfile.ZipFile('/tmp/' + filename, 'r') as z:
        z.extractall("/tmp")


def create_feature(geom, properties):
    return {
        "type": "Feature",
        'geometry': geom,
        'properties': properties
    }


def to_geojson(outfile):
    sf = shapefile.Reader("/tmp/points")

    features = []
    for index, record in enumerate(sf.records()):
        if record[3] == 'pub':
            properties = {'name': record[2]}
            features.append(create_feature(
                sf.shape(index).__geo_interface__,
                properties
            ))

    with open(outfile, 'w') as outfile:
        outfile.write(json.dumps({
            'type': 'FeatureCollection',
            'features': features
        }))


url = 'http://download.geofabrik.de/europe/norway-latest.shp.zip'
get_file(url, 'norway-latest.shp.zip')
unzip('norway-latest.shp.zip')
to_geojson('../data/pubs.geojson')
