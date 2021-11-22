import json
import os
import re

import pandas as pd
from rdflib import Namespace


class ImageService:
    def __init__(self, graph):
        self.graph = graph
        self.WD = Namespace('http://www.wikidata.org/entity/')
        self.WDT = Namespace('http://www.wikidata.org/prop/direct/')
        self.RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')

        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, '../../../../data/ddis/new_images.json'), 'r') as json_file:
            self.images_map = json.load(json_file)
        self.entity_type_map = {
            'TITLE': [self.WD.Q11424, self.WD.Q24856, self.WD.Q5398426, self.WD.Q7725310, self.WD.Q15416],
            'DIRECTOR': [self.WD.Q2526255, self.WD.Q3455803],
            'CHARACTER': [self.WD.Q95074, self.WD.Q15773347, self.WD.Q15632617],
            'ACTOR': [self.WD.Q33999, self.WD.Q10800557],
            'GENRE': [self.WD.Q483394]
        }
        print("loaded ImageService")

    def top_match(self, entities, relation):
        graph = self.graph
        entity = entities[0]
        entity_type = entity[1]
        entity_candidates = [self.WD[e] for e in entity[2]]

        targets = []
        if entity_type == 'TITLE':
            nodes = [(s, graph.value(s, self.WDT.P577), graph.value(s, self.WDT.P345).toPython()) for t in
                     self.entity_type_map[entity_type] for e in
                     entity_candidates for s, p, o in graph.triples((e, self.WDT.P31, t))
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P577) and
                     graph.value(s, self.WDT.P345) and graph.value(s, self.WDT.P345).toPython() in self.images_map]

        elif entity_type == 'GENRE':
            nodes = [(s, graph.value(s, self.WDT.P577), graph.value(s, self.WDT.P345).toPython()) for e in
                     entity_candidates for s in graph.subjects(self.WDT.P136, e)
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P577) and
                     graph.value(s, self.WDT.P345) and graph.value(s, self.WDT.P345).toPython() in self.images_map]

        elif entity_type == 'ACTOR':
            nodes = [(o, graph.value(s, self.WDT.P577), graph.value(o, self.WDT.P345).toPython()) for e in
                     entity_candidates for s, p, o in graph.triples((None, self.WDT.P161, e))
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P577) and
                     graph.value(o, self.WDT.P345) and graph.value(o, self.WDT.P345).toPython() in self.images_map]

        nodes = sorted(nodes, key=lambda tup: tup[1], reverse=True)
        if len(nodes) > 0:
            first_node = nodes[0]
            item_found = self.images_map[first_node[2]][0]
            for s, d, imdb_id in nodes[:20]:
                for item in self.images_map[imdb_id]:
                    if entity_type == 'TITLE' and re.search('actor', relation):
                        if len(item["cast"]) > 0:
                            item_found = item
                            break
                    elif entity_type == 'TITLE' and re.search('poster|posters', relation):
                        if item["type"] == "poster":
                            item_found = item
                            break
                    elif entity_type == 'ACTOR':
                        if item["type"] == "publicity":
                            item_found = item
                            break
                    else:
                        item_found = item
                        break

                if item_found:
                    targets.append((s.toPython()[len(self.WD):],
                                    graph.value(s, self.RDFS.label),
                                    item_found["img"].rstrip('.jpg')))
                    break
        df = pd.DataFrame(targets, columns=['Entity', 'EntityLabel', 'Target'])
        df = df.drop_duplicates().reset_index(drop=True)
        return df
