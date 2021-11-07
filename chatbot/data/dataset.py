import os
import rdflib


class Dataset:
    def __init__(self):
        # graph_dir = ../../../data/14_graph.nt
        dirname = os.path.dirname(__file__)
        self.graph = rdflib.Graph()
        self.graph.parse(os.path.join(dirname, '../../data/ddis/14_graph.nt'), format='turtle')
        print("Gragh is parsed!")

    def get_graph(self):
        return self.graph

