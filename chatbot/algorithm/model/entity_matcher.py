import editdistance
from rdflib import URIRef, Namespace


class EntityMatcher:
    def __init__(self, graph):
        self.graph = graph

    def top_match(self, entity):
        RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
        nodes = {}
        for node in self.graph.all_nodes():
            if isinstance(node, URIRef):
                if self.graph.value(node, RDFS.label):
                    nodes[node.toPython()] = self.graph.value(node, RDFS.label).toPython()

        tmp = 9999
        match_node = ""
        for key, value in nodes.items():
            if editdistance.eval(value, entity) < tmp:
                tmp = editdistance.eval(value, entity)
                match_node = key
        return match_node
