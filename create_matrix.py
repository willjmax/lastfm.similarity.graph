import numpy as np
import sqlite3
import itertools
from markov_cluster import *

def parse_clusters(row):
    entry_count = 0
    cluster = []
    for entry in row:
        entry_count += 1
        if entry > 0:
            cluster.append(entry_count)
        else:
            cluster.append(0)
    return cluster


conn = sqlite3.connect('lastfmgraph.db')
cur = conn.cursor()

query = "SELECT * FROM similarity"
cur.execute(query)
data = cur.fetchall()

query = "SELECT COUNT(*) FROM artists"
cur.execute(query)
number_artists = cur.fetchone()[0]

matrix = []
for _ in range(number_artists):
    row = [0.0] * number_artists
    matrix.append(row)

for tuple in data:
    matrix[tuple[0]-1][tuple[1]-1] = 1

transition_matrix = np.matrix(matrix)
np.fill_diagonal(transition_matrix, 1)
transition_matrix = run(transition_matrix)

cluster = np.apply_along_axis(parse_clusters, axis=1, arr=transition_matrix)
no_zero = cluster[~np.all(cluster == 0, axis=1)]

row_list = []

for row in no_zero:
    row_list.append(row.tolist())

row_list_no_zero_entry = []

for row in row_list:
    row_list_no_zero_entry.append([x for x in row if x != 0])

final_rows = list(k for k,_ in itertools.groupby(row_list_no_zero_entry))
cluster_count = 1
insert = []
print final_rows
query = "INSERT INTO artist_clusters VALUES (?,?)"
for cluster in final_rows:
    for artist in cluster:
        insert.append((cluster_count, artist))
    cluster_count += 1

print insert
cur.executemany(query, insert)

conn.commit()
conn.close()

