# -*- coding: utf-8 -*-

import requests
import StringIO
import unicodecsv
import json

pol_url = 'http://www.vinmonopolet.no/api/butikker'

res = requests.get(pol_url)
res.encoding = 'ISO-8859-1'


def create_feature(longitude, latitude, properties):
    return {
        'type': 'Feature',
        'geometry': {'type': 'Point', 'coordinates': [longitude, latitude]},
        'properties': properties
    }


def parse_row(row, cols):
    props = {}
    row = [col.encode('utf8') for col in row]
    for index, col in enumerate(cols):
        props[col] = row[index + 1]
    return create_feature(
        float(props.pop('GPS_lengdegrad')),
        float(props.pop('GPS_breddegrad')),
        props
    )

features = []
f = StringIO.StringIO(res.text.encode('utf8'))
reader = unicodecsv.reader(f, delimiter=';')
with open('test.txt', 'w') as out:
    cols = reader.next()[1:]
    parse_row(reader.next(), cols)
    for row in reader:
        features.append(parse_row(row, cols))


with open('../data/pol.geojson', 'w') as outfile:
    outfile.write(json.dumps({
        'type': 'FeatureCollection',
        'features': features
    }))
