# -*- coding: utf-8 -*-

import json
from flask import Flask, render_template, jsonify, request, redirect, url_for
from database import (get_pubs, get_pol, get_breweries, get_nearby_db,
                      get_feature)
import requests

app = Flask(__name__)


pages = [
    {'endpoint': 'nearby', 'title': u'I nærheten'},
    {'endpoint': 'map', 'title': 'Kart'},
    {'endpoint': 'about', 'title': u'Om ølkart'},
]


name_attrs = {
    'pol': 'Butikknavn',
    'pubs': 'name',
    'breweries': 'name'
}


@app.route('/')
def index():
    return redirect(url_for('nearby'))


@app.route('/about')
def about():
    return render_template('about.html', pages=pages)


@app.route('/nearby')
def nearby():
    return render_template(
        'nearby.html',
        pages=pages,
        name_attrs=json.dumps(name_attrs)
    )


@app.route('/map')
def map():
    maps = [
        {'title': 'Bryggerier', 'data': get_breweries(), 'id': 'breweries'},
        {'title': 'Polutsalg', 'data': get_pol(), 'id': 'pol'},
        {'title': 'Puber', 'data': get_pubs(), 'id': 'pubs'},
    ]
    return render_template(
        'map.html',
        pages=pages,
        maps=json.dumps(maps)
    )


@app.route('/route_proxy')
def route_proxy():
    url = 'https://www.vegvesen.no/ruteplan/routingservice_v1_0/routingService'
    res = requests.get(
        url + '?' + request.query_string,
        auth=('TjeRuteplanDataut', 'l0adRun3R12')
    )
    return jsonify(res.json())


@app.route('/route')
def route():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    dataset = request.args.get('dataset')
    feature = get_feature(
        dataset,
        int(request.args.get('id'))
    )

    from_pos = {'lat': lat, 'lon': lon}

    name_attr = name_attrs.get(dataset, '')

    return render_template(
        'route.html',
        pages=pages,
        from_pos=json.dumps(from_pos),
        to_feature=json.dumps(feature),
        name_attr=name_attr
    )


@app.route('/get_nearby')
def get_nearby():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    a = get_nearby_db(lat, lon)
    return jsonify(a)

if __name__ == '__main__':
    app.run(debug=True)
