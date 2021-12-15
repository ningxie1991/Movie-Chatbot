import os
import rdflib
import dill as pickle
from chatbot.algorithm.question_answering.service.crowdsource import CrowdSource


class Dataset:
    def __init__(self):
        # graph_dir = ../../../data/14_graph.nt
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, '../../data/ddis/graph.pkl'), 'rb') as file:
            self.graph = pickle.load(file)

        # self.graph = rdflib.Graph()
        # self.graph.parse(os.path.join(dirname, '../../data/ddis/14_graph.nt'), format='turtle')
        # crowd_source = CrowdSource()
        # crowd_source.merge_data(self.graph)
        print("loaded graph and merged crowd data!")

    def get_graph(self):
        return self.graph

    def dump(self):
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, '../../data/ddis/graph.pkl'), 'wb') as file:
            pickle.dump(self.graph, file)


