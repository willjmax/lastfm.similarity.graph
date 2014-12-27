import sqlite3
import pygraphviz

graph = pygraphviz.AGraph()

conn = sqlite3.connect('lastfmgraph.db')
cur = conn.cursor()

query = "SELECT artist FROM artists"
cur.execute(query)
data = cur.fetchall()
artist_array = [elt[0] for elt in data]

for artist in artist_array:
    graph.add_node(artist)

query = "SELECT a1.artist, a2.artist FROM similarity LEFT JOIN artists AS a1 ON first=a1.id LEFT JOIN artists AS a2 on second=a2.id"
cur.execute(query)
data = cur.fetchall()

for element in data:
    graph.add_edge(element[0], element[1])

graph.graph_attr.update(overlap="scale")
graph.layout()
graph.draw('big_graph.png')


