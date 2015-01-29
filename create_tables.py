import sqlite3

conn = sqlite3.connect('../lastfmgraph.db')
cur = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS artists(id INTEGER PRIMARY KEY, artist TEXT)"
cur.execute(query)

query = "CREATE TABLE IF NOT EXISTS similarity(first INTEGER, second INTEGER, UNIQUE(first, second))"
cur.execute(query)

query = "CREATE TABLE IF NOT EXISTS tags(id INTEGER PRIMARY KEY, tag TEXT)"
cur.execute(query)

query = "CREATE TABLE IF NOT EXISTS artist_tags(id INTEGER PRIMARY KEY, artist INTEGER, tag INTEGER)"
cur.execute(query)

query = "CREATE TABLE IF NOT EXISTS artist_clusters(cluster INTEGER, artist INTEGER)"
cur.execute(query)