# -*- coding: utf-8 -*-

import json
from flask import Flask, render_template, jsonify
from flask import request
from database import get_pubs, get_pol, get_breweries, get_nearby_db

app = Flask(__name__)


pages = [
    {'endpoint': 'index', 'title': 'Hjem'},
    {'endpoint': 'nearby', 'title': u'I nærheten'},
    {'endpoint': 'map', 'title': 'Kart'},
]


@app.route('/')
def index():
    return render_template('index.html', pages=pages)


@app.route('/nearby')
def nearby():
    return render_template('nearby.html', pages=pages)


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


@app.route('/get_nearby')
def get_nearby():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    a = get_nearby_db(lat, lon)
    print a
    return jsonify(a)

if __name__ == '__main__':
    app.run(debug=True)
