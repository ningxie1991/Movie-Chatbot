import csv
import os
import re

import numpy as np
import pandas as pd
import rdflib
from rdflib import Namespace
from sklearn.metrics import pairwise_distances


class RecommenderService:
    def __init__(self, graph):
        self.graph = graph
        self.WD = Namespace('http://www.wikidata.org/entity/')
        self.WDT = Namespace('http://www.wikidata.org/prop/direct/')
        self.RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')

        # load the embeddings
        dirname = os.path.dirname(__file__)
        self.entity_emb = np.load(os.path.join(dirname, '../../../../data/ddis/entity_embeds.npy'))
        self.relation_emb = np.load(os.path.join(dirname, '../../../../data/ddis/relation_embeds.npy'))

        # load the dictionaries
        with open(os.path.join(dirname, '../../../../data/ddis/entity_ids.del'), 'r') as ifile:
            self.ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
            self.id2ent = {v: k for k, v in self.ent2id.items()}
        with open(os.path.join(dirname, '../../../../data/ddis/relation_ids.del'), 'r') as ifile:
            self.rel2id = {rdflib.term.URIRef(rel): int(idx) for idx, rel in csv.reader(ifile, delimiter='\t')}
            self.id2rel = {v: k for k, v in self.rel2id.items()}
        self.ent2lbl = {ent: str(lbl) for ent, lbl in graph.subject_objects(self.RDFS.label)}
        self.lbl2ent = {lbl: ent for ent, lbl in self.ent2lbl.items()}

        # define entity type and predicate maps
        self.entity_type_map = {
            'TITLE': [self.WD.Q11424, self.WD.Q24856, self.WD.Q5398426, self.WD.Q7725310, self.WD.Q15416],
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
        print("loaded RecommenderService")

    def top_match(self, entities, relation):
        graph = self.graph
        entity = entities[0]
        entity_type = entity[1]
        entity_candidates = [self.WD[e] for e in entity[2]]

        if re.search("movie|film", relation):
            predicate = self.entity_predicate_map['TITLE']
        elif re.search("director", relation):
            predicate = self.entity_predicate_map['DIRECTOR']
        elif re.search("character", relation):
            predicate = self.entity_predicate_map['CHARACTER']
        elif re.search("actor", relation):
            predicate = self.entity_predicate_map['ACTOR']
        else:
            predicate = self.entity_predicate_map[entity_type]
        nodes = [(s, p, o) for t in self.entity_type_map[entity_type] for e in entity_candidates for s, p, o in graph.triples((e, predicate, t))]

        targets = []
        for s, p, o in nodes:
            ent = self.ent2id[s]
            # we compare the embedding of the query entity to all other entity embeddings
            dist = pairwise_distances(self.entity_emb[ent].reshape(1, -1), self.entity_emb).reshape(-1)
            # order by plausibility
            most_likely = dist.argsort()
            top_match = [
                (
                    self.id2ent[idx][len(self.WD):],  # qid
                    self.ent2lbl[self.id2ent[idx]],  # label
                    dist[idx],  # score
                    rank + 1,  # rank
                )
                for rank, idx in enumerate(most_likely[:5])]
            if len(top_match) > 0:
                targets += top_match
                break
        df = pd.DataFrame(targets, columns=['Target', 'TargetLabel', "Score", "Rank"])
        df = df[df.Score != 0].drop_duplicates().sort_values(by='Score', na_position='last').reset_index(drop=True)
        return df[:30]

