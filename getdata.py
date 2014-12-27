import sqlite3
import sys
import keys
import pylast

conn = sqlite3.connect('lastfmgraph.db')
cur = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS artists(id INTEGER PRIMARY KEY, artist TEXT)"
cur.execute(query)

query = "CREATE TABLE IF NOT EXISTS similarity(first INTEGER, second INTEGER, UNIQUE(first, second))"
cur.execute(query)

query = "SELECT COUNT(*) FROM artists"
cur.execute(query)
number = cur.fetchone()[0]

query = "SELECT artist FROM artists"
cur.execute(query)
data = cur.fetchall()
current_artists = [elt[0] for elt in data]

network = pylast.get_lastfm_network(keys.api_key, keys.api_secret, keys.user, keys.password)
user = pylast.User(sys.argv[1], network)
top_artists = user.get_top_artists(limit=50)

query = "INSERT INTO artists VALUES (?,?)"
count = 1
insert = []
for artist in top_artists:
    name = artist.item.get_name()
    if name not in current_artists:
        insert.append((count+number, name))
        count += 1

cur.executemany(query, insert)

query = "SELECT * FROM artists"
cur.execute(query)
data = cur.fetchall()
artist_array = [elt[1] for elt in data]
all_artists = {}
for artist in data:
    all_artists[artist[1]] = artist[0]


query = "INSERT OR IGNORE INTO similarity VALUES (?,?)"
insert = []
for artist in top_artists:
    name = artist.item.get_name()
    print name
    similar = artist.item.get_similar()
    similar_array = []
    for sim in similar:
        sim_artist = sim.item.get_name()
        if sim_artist in artist_array:
            insert.append((all_artists[name], all_artists[sim_artist]))

cur.executemany(query, insert)

conn.commit()
conn.close()