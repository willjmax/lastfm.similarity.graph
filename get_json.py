import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('lastfmgraph.db')
conn.row_factory = dict_factory

cur = conn.cursor()
query = "SELECT (a1.id - 1) AS source, (a2.id - 1) AS target FROM similarity LEFT JOIN artists AS a1 ON first=a1.id LEFT JOIN artists AS a2 on second=a2.id"
cur.execute(query)
links = cur.fetchall()

query = "SELECT artist AS name FROM artists"
cur.execute(query)
nodes = cur.fetchall()

data = {"nodes": nodes, "links": links}

with open("similarity.json", "w") as fh:
    fh.write(json.dumps(data))

conn.close()
