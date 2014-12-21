import pygraphviz as pgv
import pylast
import keys
import sys

class Artist:
    name = ""
    similar = []

    def __init__(self, name, similar):
        self.name = name
        self.similar = similar
        print self.name

network = pylast.get_lastfm_network(keys.api_key, keys.api_secret, keys.user, keys.password)

user = pylast.User(sys.argv[1], network)
graph = pgv.AGraph()
top_artists = user.get_top_artists(limit=50)
artist_array = []
for artist in top_artists:
    similar = artist.item.get_similar()
    similar_array = []
    for sim_artist in similar:
        similar_array.append(sim_artist.item.get_name())
    artist_array.append(Artist(artist.item.get_name(), similar_array))
    graph.add_node(artist.item.get_name())

for counter, artist in enumerate(artist_array):
    for art in artist_array[counter:]:
        if artist.name in art.similar:
            graph.add_edge(artist.name, art.name)

graph.graph_attr.update(overlap="scale")
graph.layout()
graph.draw('graph.png')

