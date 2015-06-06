# -*- coding: utf-8 -*-

import requests
import re

import psycopg2
from psycopg2.extras import RealDictCursor


def save(population):
    conn = psycopg2.connect('dbname=beer user=atlefren password=atlefren')
    conn.cursor_factory = RealDictCursor

    cur = conn.cursor()
    cur.executemany(
        """INSERT INTO population(komm, population) VALUES (%(komm)s, %(population)s)""",
        population
    )
    conn.commit()
    cur.close()
    conn.close()


def parse_row(row, cols):
    props = {}
    row = [col for col in row]
    for index, col in enumerate(cols):
        props[col] = row[index + 1]
    return props


url = 'https://www.ssb.no/eksport/tabell.csv?key=227581'

res = requests.get(url)

lines = res.text.splitlines()

p = re.compile('([0-9]{4})')
lines.pop()

res = []
for line in lines:
    s = line.split(';')
    m = p.match(s[0])
    if m:
        res.append({'komm': m.group(), 'population': float(s[11])})

save(tuple(res))
