import datetime
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
        with open(os.path.join(dirname, '../../../../data/ddis/images.json'), 'r') as json_file:
            self.images_map = json.load(json_file)
        self.entity_type_map = {
            'TITLE': [self.WD.Q11424, self.WD.Q24856],
            # self.WD.Q5398426, self.WD.Q7725310, self.WD.Q15416],
            'DIRECTOR': [self.WD.Q2526255, self.WD.Q3455803],
            'CHARACTER': [self.WD.Q95074, self.WD.Q15773347, self.WD.Q15632617],
            'ACTOR': [self.WD.Q33999, self.WD.Q10800557],
            'GENRE': [self.WD.Q483394]
        }
        self.entity_predicate_map = {
            'TITLE': self.WDT.P31,
            'DIRECTOR': self.WDT.P106,
            'CHARACTER': self.WDT.P31,
            'ACTOR': self.WDT.P106,
            'GENRE': self.WDT.P31
        }

    def top_match(self, entities, relation):
        graph = self.graph
        entity = entities[0]
        entity_type = entity[1]
        entity_candidates = [self.WD[e] for e in entity[2]]

        targets = []
        if entity_type == 'GENRE':
            nodes = [(s, graph.value(s, self.WDT.P577)) for e1 in entity_candidates for s in
                     graph.subjects(self.WDT.P136, e1)
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P345)]
        else:
            nodes = [(s, graph.value(s, self.WDT.P577)) for t in self.entity_type_map[entity_type] for e in
                     entity_candidates for s, p, o in graph.triples((e, self.entity_predicate_map[entity_type], t))
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P345)]

        nodes = [(s, d) for s, d in nodes if d is not None and d.toPython() < datetime.date(2020, 6, 1)]
        nodes = sorted(nodes, key=lambda tup: tup[1], reverse=True)
        item_found = None
        for s, d in nodes[:30]:
            imdb_id = graph.value(s, self.WDT.P345).toPython()
            try:
                if entity_type == 'TITLE' and re.search('actor', relation):
                    item_found = next(
                        item for item in self.images_map if imdb_id in item["movie"] and len(item["cast"]) > 0)
                elif re.search('poster|posters', relation):
                    item_found = next(
                        item for item in self.images_map if imdb_id in item["movie"] and item["type"] == "poster")
                else:
                    item_found = next(item for item in self.images_map if imdb_id in item["movie"] or imdb_id in item["cast"])
            except Exception as e:
                print("Error:", e)
            if item_found:
                targets.append((s.toPython()[len(self.WD):],
                                graph.value(s, self.RDFS.label),
                                item_found["img"].rstrip('.jpg'),
                                d.toPython()))
                break
        df = pd.DataFrame(targets, columns=['Entity', 'EntityLabel', 'Target', 'Date'])
        df = df.drop_duplicates().reset_index(drop=True)
        return df[:30]
