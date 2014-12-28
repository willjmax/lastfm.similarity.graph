import pygraphviz as pgv
import pylast
import keys
import sys


class Artist:
    name = ""
    similar = []
    tags = []

    def __init__(self, name, similar, tags):
        self.name = name
        self.similar = similar
        self.tags = tags


def top_tag(artist1, artist2):
    tag1 = artist1.tags
    tag2 = artist2.tags
    sim_tags = []

    for tag in tag1:
        if tag in tag2:
            sim_tags.append(tag)

    return sim_tags[0]



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
    tags = artist.item.get_top_tags()
    tags_array = []
    for tag in tags:
        tags_array.append(tag.item.get_name())
    artist_array.append(Artist(artist.item.get_name(), similar_array, tags_array))
    graph.add_node(artist.item.get_name())

for counter, artist in enumerate(artist_array):
    for art in artist_array:
        if artist.name in art.similar:
            graph.add_edge(artist.name, art.name)
            edge = graph.get_edge(artist.name, art.name)
            edge.attr['label'] = top_tag(artist, art)
            edge.attr['labelfloat'] = False
            print artist.name, art.name, top_tag(artist, art)


graph.graph_attr.update(overlap="scale")
graph.layout()
graph.draw('graph.png')

