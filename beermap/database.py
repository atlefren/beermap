# -*- coding: utf-8 -*-
import json
import psycopg2
from psycopg2.extras import RealDictCursor


conn = psycopg2.connect('dbname=beer user=atlefren password=atlefren')
conn.cursor_factory = RealDictCursor


column_list = {
    'pol': ['apn_tirsdag', 'apn_torsdag', 'butikknavn',
            'kategori', 'gate_poststed', 'post_postnummer',
            'gate_postnummer', 'apn_onsdag', 'apn_lordag',
            'gateadresse', 'postadresse', 'post_poststed', 'apn_fredag',
            'apn_mandag'],
    'breweries': ['website', 'name', 'street', 'address',
                  'comment', 'phone', 'org_desc'],
    'pubs': ['name'],
    'hex': []
}


def create_featurecollection(features):
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def parse_row(row):

    geom = json.loads(row.pop('geom'))
    return {
        'type': 'Feature',
        'geometry': geom,
        'properties': row
    }


def get_feature(table, id):
    cur = conn.cursor()

    sql = '''
        SELECT *, ST_AsGeoJSON(wkb_geometry) as geom, ogc_fid as id
        FROM {0}
        WHERE ogc_fid = {1:d}
    '''.format(table, id)
    cur.execute(sql)
    d = parse_row(cur.fetchone())
    cur.close()
    return d


def get_table(table, columns):
    cur = conn.cursor()
    cols = ''
    if len(columns):
        cols = ', '.join(columns) + ','
    sql = '''
        SELECT {0} ST_AsGeoJSON(wkb_geometry) as geom, ogc_fid as id FROM {1}
    '''.format(cols, table)

    print sql
    cur.execute(sql)
    features = [parse_row(row) for row in cur.fetchall()]
    cur.close()
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def get_data(table):
    return get_table(table, column_list[table])


def get_breweries():
    return get_data('breweries')


def get_pol():
    return get_data('pol')


def get_pubs():
    return get_data('pubs')


def get_ten_closest(table, lat, lon):

    columns = column_list[table]

    cur = conn.cursor()
    sql = '''
        SELECT
            {0},
            ST_AsGeoJSON(wkb_geometry) as geom,
            ST_Distance(st_setsrid(st_makepoint({1:f}, {2:f}), 4326)::geography,
            wkb_geometry::geography) / 1000 as distance,
            ogc_fid as id
        FROM
            {3}
        ORDER BY
            distance
        LIMIT 10
    '''.format(','.join(columns), lon, lat, table)

    cur.execute(sql)

    features = [parse_row(row) for row in cur.fetchall()]
    cur.close()
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def group_by_kommune(table):
    cur = conn.cursor()
    sql = '''
        SELECT kommuner.navn, kommuner.komm, count(*) AS num
        FROM kommuner, {0}
        WHERE st_intersects(kommuner.wkb_geometry, {0}.wkb_geometry)
        GROUP BY kommuner.komm, kommuner.navn
        order by num DESC'''.format(table)

    cur.execute(sql)

    res = cur.fetchall()
    cur.close()
    return res


def get_hex(table):
    cur = conn.cursor()
    sql = '''
    SELECT
        ST_AsGeoJSON(hex.wkb_geometry) as geom,
        COUNT({0}.ogc_fid) AS count
    FROM hex 
      LEFT JOIN {0} ON st_contains(hex.wkb_geometry, {0}.wkb_geometry)
    GROUP BY hex.wkb_geometry
    ORDER BY count DESC
    '''.format(table)
    cur.execute(sql)

    features = [parse_row(row) for row in cur.fetchall()]
    cur.close()
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def get_kommune_stats():
    return {
        'pol': group_by_kommune('pol'),
        'pubs': group_by_kommune('pubs'),
        'breweries': group_by_kommune('breweries'),
        'hex': {
            'pol': get_hex('pol'),
            'pubs': get_hex('pubs'),
            'breweries': get_hex('breweries')
        }
    }


def get_nearby_db(lat, lon):
    return {
        'pol': get_ten_closest('pol', lat, lon),
        'pubs': get_ten_closest('pubs', lat, lon),
        'breweries': get_ten_closest('breweries', lat, lon),
    }
