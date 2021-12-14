import re
import time
import pandas as pd
from rdflib import Namespace, URIRef
from chatbot.algorithm.predicate_linker import PredicateLinker
from chatbot.algorithm.question_answering.service.embedding import EmbeddingService


class RDFQueryService:
    def __init__(self, graph):
        self.graph = graph
        self.predicate_linker = PredicateLinker()
        self.embedding_service = EmbeddingService(graph)
        self.WD_uri = 'http://www.wikidata.org/entity/'
        self.WD = Namespace(self.WD_uri)
        self.WDT_uri = 'http://www.wikidata.org/prop/direct/'
        self.WDT = Namespace(self.WDT_uri)
        self.RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
        self.DDIS_uri = 'http://ddis.ch/atai/'
        self.DDIS = Namespace(self.DDIS_uri)
        self.entity_predicate_map = {
            'TITLE': [self.WDT.P161, self.WDT.P1441],
            'DIRECTOR': [self.WDT.P57],
            'CHARACTER': [self.WDT.P1441, self.WDT.P674],
            'ACTOR': [self.WDT.P161, self.WDT.P175],
            'GENRE': [self.WDT.P136]
        }
        self.columns = ['Subject', 'SubjectLabel', 'Relation', 'RelationLabel', 'Object', 'ObjectLabel', 'Date']
        print("RDFQueryService initialized")

    def format_subject(self, s):
        s_uri = re.sub(self.WD_uri, "wd:", s.toPython())
        s_label = self.graph.value(s, self.RDFS.label).toPython() if self.graph.value(s, self.RDFS.label) else s_uri
        return s_uri, s_label

    def format_predicate(self, p):
        if re.search(self.DDIS_uri, p):
            p_uri = re.sub(self.DDIS_uri, "ddis:", p.toPython())
        else:
            p_uri = re.sub(self.WDT_uri, "wdt:", p.toPython())
        p_label = self.graph.value(p, self.RDFS.label).toPython() if self.graph.value(p, self.RDFS.label) else p_uri
        return p_uri, p_label

    def format_object(self, o):
        if isinstance(o, URIRef):
            o_uri = re.sub(self.WD_uri, "wd:", o.toPython())
            o_label = self.graph.value(o, self.RDFS.label).toPython() if self.graph.value(o, self.RDFS.label) else o_uri
        else:
            o_uri = o.toPython()
            o_label = o.toPython()
        return str(o_uri), str(o_label)

    def query_wh(self, entities, relation):
        graph = self.graph
        entity = entities[0]
        entity_candidates = [self.WD[e] for e in entity[2]['primary']]
        entity_candidates_secondary = [self.WD[e] for e in entity[2]['secondary']]

        targets = []
        outbound = []
        inbound = []
        if relation:
            matched_pred = self.predicate_linker.top_match(relation)[0]
            predicate = URIRef(matched_pred[0])
            for e in entity_candidates:
                outbound += [(s, p, o) for s, p, o in graph.triples((e, predicate, None))]
                inbound += [(s, p, o) for s, p, o in graph.triples((None, predicate, e))]

            if len(outbound) == 0 and len(inbound) == 0:
                for e in entity_candidates_secondary:
                    outbound += [(s, p, o) for s, p, o in graph.triples((e, predicate, None))]
                    inbound += [(s, p, o) for s, p, o in graph.triples((None, predicate, e))]

            if predicate == self.WDT.P31 or re.search("type|class|parent|indirectSubclassOf|sub class", relation):
                for s, p, o in outbound:
                    if graph.value(s, self.RDFS.label):
                        s_uri, s_label = self.format_subject(s)
                        p_uri, p_label = self.format_predicate(p)
                        o_uri, o_label = self.format_object(o)
                        targets.append((s_uri, s_label,
                                        p_uri, p_label,
                                        o_uri, o_label,
                                        graph.value(s, self.WDT.P577)))
                if len(targets) == 0:
                    for e in entity_candidates:
                        s_uri, s_label = self.format_subject(e)
                        type = self.embedding_service.find_type(e)
                        if type:
                            targets.append((s_uri, s_label,
                                            "ddis:indirectSubclassOf", "indirectSubclassOf",
                                            type[0], type[1],
                                            None))
            else:
                for s, p, o in outbound + inbound:
                    if graph.value(s, self.RDFS.label):
                        s_uri, s_label = self.format_subject(s)
                        p_uri, p_label = self.format_predicate(p)
                        o_uri, o_label = self.format_object(o)
                        targets.append((s_uri, s_label,
                                        p_uri, p_label,
                                        o_uri, o_label,
                                        graph.value(s, self.WDT.P577)))

        df = pd.DataFrame(targets, columns=self.columns)
        df = df.drop_duplicates().sort_values(by='Date', ascending=False, na_position='last').reset_index(drop=True)
        return df[:30]

    def query_yesno(self, entities):
        graph = self.graph
        targets = []
        if len(entities) > 1:
            entity1 = entities[0]
            entity2 = entities[1]
            entity1_candidates_primary = [self.WD[e] for e in entity1[2]['primary']]
            entity1_candidates_secondary = [self.WD[e] for e in entity1[2]['secondary']]
            entity2_candidates_primary = [self.WD[e] for e in entity2[2]['primary']]
            entity2_candidates_secondary = [self.WD[e] for e in entity2[2]['secondary']]

            entity1_candidates = entity1_candidates_primary + entity1_candidates_secondary
            entity2_candidates = entity2_candidates_primary + entity2_candidates_secondary

            outbound = []
            inbound = []
            for e1, e2 in [(e1, e2) for e1 in entity1_candidates_primary for e2 in entity2_candidates_primary]:
                outbound += [(s, p, o) for s, p, o in graph.triples((e1, None, e2))]
                inbound += [(s, p, o) for s, p, o in graph.triples((e2, None, e1))]

            outbound_2 = []
            inbound_2 = []
            for e1, e2 in [(e1, e2) for e1 in entity1_candidates for e2 in entity2_candidates]:
                outbound_2 += [(s, p, o) for s, p, o in graph.triples((e1, None, e2))]
                inbound_2 += [(s, p, o) for s, p, o in graph.triples((e2, None, e1))]

            if len(outbound) == 0 and len(inbound) == 0:
                outbound = outbound_2
                inbound = inbound_2

            for s, p, o in outbound:
                if graph.value(s, self.RDFS.label) and graph.value(p, self.RDFS.label) and graph.value(o, self.RDFS.label):
                    s_uri, s_label = self.format_subject(s)
                    p_uri, p_label = self.format_predicate(p)
                    o_uri, o_label = self.format_object(o)
                    targets.append((s_uri, s_label,
                                    p_uri, p_label,
                                    o_uri, o_label,
                                    graph.value(s, self.WDT.P577)))

            for s, p, o in inbound:
                if graph.value(s, self.RDFS.label) and graph.value(p, self.RDFS.label) and graph.value(o, self.RDFS.label):
                    s_uri, s_label = self.format_subject(s)
                    p_uri, p_label = self.format_predicate(p)
                    o_uri, o_label = self.format_object(o)
                    targets.append((o_uri, o_label,
                                    p_uri, p_label,
                                    s_uri, s_label,
                                    graph.value(s, self.WDT.P577)))

        df = pd.DataFrame(targets, columns=['Subject', 'SubjectLabel', 'Relation', 'RelationLabel', 'Object', 'ObjectLabel', 'Date'])
        df = df.drop_duplicates().sort_values(by='Date', ascending=False, na_position='last').reset_index(drop=True)
        return df[:30]

    def query_action(self, entities):
        graph = self.graph
        targets = []
        if len(entities) == 1:
            entity = entities[0]
            entity_type = entity[1]
            entity_candidates = [self.WD[e] for e in entity[2]['primary']]
            if entity_type == 'GENRE':
                start_time = time.time()
                genre_candidates = [s for e in entity_candidates for s, p, o in
                                    graph.triples((e, self.WDT.P31, self.WD.Q201658))]
                for s in [s for e1 in genre_candidates[:5] for pred in self.entity_predicate_map[entity_type] for s in graph.subjects(pred, e1)]:
                    if graph.value(s, self.RDFS.label):
                        s_uri, s_label = self.format_subject(s)
                        targets.append((s_uri, s_label,
                                        graph.value(s, self.WDT.P577)))
                print("---Took %s seconds to get all nodes---" % (time.time() - start_time))
            else:
                for s in [s for e1 in entity_candidates for pred in self.entity_predicate_map[entity_type] for s in graph.subjects(pred, e1)]:
                    if graph.value(s, self.RDFS.label):
                        s_uri, s_label = self.format_subject(s)
                        targets.append((s_uri, s_label,
                                        graph.value(s, self.WDT.P577)))

        else:
            entity1 = entities[0]
            entity2 = entities[1]
            entity1_type = entity1[1]
            entity2_type = entity2[1]

            entity1_candidates = [self.WD[e] for e in entity1[2]['primary']]
            entity1_candidates_secondary = [self.WD[e] for e in entity1[2]['secondary']]
            entity2_candidates = [self.WD[e] for e in entity2[2]['primary']]
            entity2_candidates_secondary = [self.WD[e] for e in entity2[2]['secondary']]

            nodes = [s for e1 in entity1_candidates for pred in self.entity_predicate_map[entity1_type] for s in graph.subjects(pred, e1)]
            if len(nodes) == 0:
                nodes = [s for e1 in entity1_candidates_secondary for pred in self.entity_predicate_map[entity1_type] for s in
                         graph.subjects(pred, e1)]

            new_nodes = [(node, pred, e2) for node in nodes for pred in self.entity_predicate_map[entity2_type] for e2 in entity2_candidates]
            if len(new_nodes) == 0:
                new_nodes = [(node, pred, e2) for node in nodes for pred in self.entity_predicate_map[entity2_type] for e2 in entity2_candidates_secondary]

            for node, pred, e2 in new_nodes:
                for s, p, o in graph.triples((node, pred, e2)):
                    if graph.value(s, self.RDFS.label):
                        s_uri, s_label = self.format_subject(s)
                        targets.append((s_uri, s_label,
                                        graph.value(s, self.WDT.P577)))

        df = pd.DataFrame(targets, columns=['Target', 'TargetLabel', "Date"])
        df = df.drop_duplicates().sort_values(by='Date', ascending=False, na_position='last').reset_index(drop=True)
        return df[:30]