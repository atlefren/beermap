import json
from flask import Flask, render_template
app = Flask(__name__)


pages = [
    {'endpoint': 'index', 'title': 'Hjem'},
    {'endpoint': 'map', 'title': 'Kart'},
]


def get_data(filename):
    with open('data/' + filename) as file:
        return file.read()


@app.route('/')
def index():
    return render_template('index.html', pages=pages)


@app.route('/map')
def map():

    breweries = json.loads(get_data('breweries.geojson'))

    maps = [
        {'title': 'Bryggerier', 'data': breweries, 'id': 'breweries'},
    ]

    return render_template(
        'map.html',
        pages=pages,
        maps=json.dumps(maps)
    )

if __name__ == '__main__':
    app.run(debug=True)
