import rdflib


class Dataset:
    def __init__(self, graph_dir):
        self.graph = rdflib.Graph()
        self.graph.parse(graph_dir, format='turtle')

    def get_graph(self):
        return self.graph

