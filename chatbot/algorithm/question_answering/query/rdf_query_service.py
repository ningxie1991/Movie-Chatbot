import pandas as pd
from rdflib import Namespace, URIRef
from chatbot.algorithm.predicate_linker import PredicateLinker


class RDFQueryService:
    def __init__(self, graph):
        self.graph = graph
        self.predicate_linker = PredicateLinker()
        self.WD = Namespace('http://www.wikidata.org/entity/')
        self.WDT = Namespace('http://www.wikidata.org/prop/direct/')
        self.RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
        self.entity_predicate_map = {
            'TITLE': [self.WDT.P161, self.WDT.P1441],
            'DIRECTOR': [self.WDT.P57],
            'CHARACTER': [self.WDT.P1441, self.WDT.P674],
            'ACTOR': [self.WDT.P161, self.WDT.P175],
            'GENRE': [self.WDT.P136]
        }
        self.columns = ['Entity', 'EntityLabel', 'Target', 'TargetLabel', "Date"]
        print("loaded RDFQueryService")

    def query_wh(self, entities, relation):
        graph = self.graph
        entity = entities[0]
        entity_candidates = [self.WD[e] for e in entity[2]]
        matched_pred = self.predicate_linker.top_match(relation)[0]
        print(f"relation: {relation}, matched_pred: {matched_pred}")

        targets = []
        predicate = URIRef(matched_pred[0])
        for e in entity_candidates:
            outbound = [(s, p, o) for s, p, o in graph.triples((e, predicate, None))]
            inbound = [(s, p, o) for s, p, o in graph.triples((None, predicate, e))]
            for s, p, o in outbound + inbound:
                if graph.value(s, self.RDFS.label) and graph.value(o, self.RDFS.label):
                    targets.append((s.toPython()[len(self.WD):],
                                    graph.value(s, self.RDFS.label).toPython(),
                                    o.toPython()[len(self.WD):],
                                    graph.value(o, self.RDFS.label).toPython(),
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
            entity1_candidates = [self.WD[e] for e in entity1[2]]
            entity2_candidates = [self.WD[e] for e in entity2[2]]

            for e1, e2 in [(e1, e2) for e1 in entity1_candidates for e2 in entity2_candidates]:
                outbound = [(s, p, o) for s, p, o in graph.triples((e1, None, e2))]
                for s, p, o in outbound:
                    if graph.value(s, self.RDFS.label) and graph.value(p, self.RDFS.label) and graph.value(o, self.RDFS.label):
                        targets.append((s.toPython()[len(self.WD):],
                                        graph.value(s, self.RDFS.label).toPython(),
                                        p.toPython()[len(self.WDT):],
                                        graph.value(p, self.RDFS.label).toPython(),
                                        o.toPython()[len(self.WD):],
                                        graph.value(o, self.RDFS.label).toPython(),
                                        graph.value(s, self.WDT.P577)))

                inbound = [(s, p, o) for s, p, o in graph.triples((e2, None, e1))]
                for s, p, o in inbound:
                    if graph.value(s, self.RDFS.label) and graph.value(p, self.RDFS.label) and graph.value(o, self.RDFS.label):
                        targets.append((o.toPython()[len(self.WD):],
                                        graph.value(o, self.RDFS.label).toPython(),
                                        p.toPython()[len(self.WDT):],
                                        graph.value(p, self.RDFS.label).toPython(),
                                        s.toPython()[len(self.WD):],
                                        graph.value(s, self.RDFS.label).toPython(),
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
            entity_candidates = [self.WD[e] for e in entity[2]]
            for s in [s for e1 in entity_candidates for pred in self.entity_predicate_map[entity_type] for s in graph.subjects(pred, e1)]:
                if graph.value(s, self.RDFS.label):
                    targets.append((s.toPython()[len(self.WD):],
                                    graph.value(s, self.RDFS.label).toPython(),
                                    graph.value(s, self.WDT.P577)))

        else:
            entity1 = entities[0]
            entity2 = entities[1]
            entity1_type = entity1[1]
            entity2_type = entity2[1]
            entity1_candidates = [self.WD[e] for e in entity1[2]]
            entity2_candidates = [self.WD[e] for e in entity2[2]]
            nodes = [s for e1 in entity1_candidates for pred in self.entity_predicate_map[entity1_type] for s in graph.subjects(pred, e1)]
            for node, pred, e2 in [(node, pred, e2) for node in nodes for pred in self.entity_predicate_map[entity2_type] for e2 in entity2_candidates]:
                for s, p, o in graph.triples((node, pred, e2)):
                    if graph.value(s, self.RDFS.label):
                        targets.append((s.toPython()[len(self.WD):],
                                        graph.value(s, self.RDFS.label).toPython(),
                                        graph.value(s, self.WDT.P577)))

        df = pd.DataFrame(targets, columns=['Target', 'TargetLabel', "Date"])
        df = df.drop_duplicates().sort_values(by='Date', ascending=False, na_position='last').reset_index(drop=True)
        return df[:30]