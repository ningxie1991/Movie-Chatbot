import json
import os
import re
import time
import pandas as pd
from rdflib import Namespace


class ImageService:
    def __init__(self, graph):
        self.graph = graph
        self.WD_uri = 'http://www.wikidata.org/entity/'
        self.WD = Namespace(self.WD_uri)
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
            'GENRE': [self.WD.Q201658]  # film genre Q201658
        }
        print("ImageService initialized")

    def top_match(self, entities, relation):
        graph = self.graph
        entity = entities[0]
        entity_type = entity[1]
        entity_candidates = [self.WD[e] for e in entity[2]['primary'] + entity[2]['secondary']]

        targets = []
        if entity_type == 'TITLE':
            nodes = [(s, graph.value(s, self.WDT.P577), graph.value(s, self.WDT.P345).toPython()) for t in
                     self.entity_type_map[entity_type] for e in
                     entity_candidates for s, p, o in graph.triples((e, self.WDT.P31, t))
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P577) and
                     graph.value(s, self.WDT.P345) and graph.value(s, self.WDT.P345).toPython() in self.images_map]

        elif entity_type == 'GENRE':
            start_time = time.time()
            genre_candidates = [s for e in entity_candidates for s, p, o in
                                graph.triples((e, self.WDT.P31, self.WD.Q201658))]

            nodes = [(s, graph.value(s, self.WDT.P577), graph.value(s, self.WDT.P345).toPython()) for e in
                     genre_candidates[:5] for s in graph.subjects(self.WDT.P136, e)
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P577) and
                     graph.value(s, self.WDT.P345) and graph.value(s, self.WDT.P345).toPython() in self.images_map]
            # print("---Took %s seconds to get all nodes---" % (time.time() - start_time))

        elif entity_type == 'ACTOR':
            nodes = [(o, graph.value(s, self.WDT.P577), graph.value(o, self.WDT.P345).toPython()) for e in
                     entity_candidates for s, p, o in graph.triples((None, self.WDT.P161, e))
                     if graph.value(s, self.RDFS.label) and graph.value(s, self.WDT.P577) and
                     graph.value(o, self.WDT.P345) and graph.value(o, self.WDT.P345).toPython() in self.images_map]

        nodes = sorted(nodes, key=lambda tup: tup[1], reverse=True)
        start_time = time.time()
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
                    s_uri, s_label = self.format_subject(s)
                    targets.append((s_uri, s_label, item_found["img"].rstrip('.jpg')))
                    break
        # print("---Took %s seconds to find an image---" % (time.time() - start_time))
        df = pd.DataFrame(targets, columns=['Entity', 'EntityLabel', 'Target'])
        df = df.drop_duplicates().reset_index(drop=True)
        return df

    def format_subject(self, s):
        s_uri = re.sub(self.WD_uri, "wd:", s.toPython())
        s_label = self.graph.value(s, self.RDFS.label).toPython() if self.graph.value(s, self.RDFS.label) else s_uri
        return s_uri, s_label
