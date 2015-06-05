# -*- coding: utf-8 -*-
import json
from haversine import haversine


def get_data(filename):
    with open('data/' + filename) as file:
        fc = json.loads(file.read())
        for index, feature in enumerate(fc['features']):
            feature['properties']['id'] = index + 1
        return fc

breweries = get_data('breweries.geojson')
pol = get_data('pol.geojson')
pubs = get_data('pubs.geojson')

datasets = {
    'breweries': breweries,
    'pol': pol,
    'pubs': pubs
}


def get_feature(dataset, id):
    fc = datasets.get(dataset)
    for feature in fc['features']:
        if feature['properties']['id'] == id:
            return feature


def create_featurecollection(features):
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def get_pubs():
    return pubs


def get_pol():
    return pol


def get_breweries():
    return breweries


def get_ten_closest(featurecollection, lat, lon):
    pos = (lon, lat)

    for feature in featurecollection['features']:
        p = (
            feature['geometry']['coordinates'][0],
            feature['geometry']['coordinates'][1]
        )
        feature['properties']['distance'] = haversine(pos, p)

    return create_featurecollection(
        sorted(
            featurecollection['features'],
            key=lambda k: k['properties']['distance']
        )[:10]
    )


def get_nearby_db(lat, lon):
    return {
        'pol': get_ten_closest(pol, lat, lon),
        'pubs': get_ten_closest(pubs, lat, lon),
        'breweries': get_ten_closest(breweries, lat, lon),
    }
