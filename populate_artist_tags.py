import keys
import pylast
import sqlite3



conn = sqlite3.connection("lastfmdb.db")
cur = conn.cursor()

query = "SELECT * FROM tags"
tags = cur.fetchall()

query = "SELECT * FROM artist_tags"
artist_tags = cur.fetchall()


