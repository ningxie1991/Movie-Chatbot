import os
import rdflib

from chatbot.algorithm.question_answering.service.crowdsource import CrowdSource


class Dataset:
    def __init__(self):
        # graph_dir = ../../../data/14_graph.nt
        dirname = os.path.dirname(__file__)
        self.graph = rdflib.Graph()
        self.graph.parse(os.path.join(dirname, '../../data/ddis/14_graph.nt'), format='turtle')
        crowd_source = CrowdSource()
        crowd_source.merge_data(self.graph)
        print("loaded graph and merged crowd data!")

    def get_graph(self):
        return self.graph


