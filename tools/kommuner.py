# -*- coding: utf-8 -*-
import requests
import json

url = 'http://knreise.cartodb.com/api/v2/sql'
url += '?api_key=e6b96c1e6a71b8b2c6f8dbb611c08da5842f5ff5'
url += '&q=SELECT navn, komm, ST_AsGeoJSON(the_geom) as geom from kommuner'

r = requests.get(url)

data = r.json()

features = []
for row in data['rows']:
    geom = row.pop('geom')
    print row
    features.append({
        "type": "Feature",
        "geometry": json.loads(geom),
        "properties": row
    })

with open('../data/kommuner.geojson', 'w') as f:
    f.write(json.dumps({
        'type': 'FeatureCollection',
        'features': features
    }))
