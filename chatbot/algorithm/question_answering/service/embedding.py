import csv
import os
import re

import numpy as np
import pandas as pd
import rdflib
from rdflib import Namespace
from sklearn.metrics import pairwise_distances


class EmbeddingService:
    def __init__(self, graph):
        self.graph = graph
        self.WD_uri = 'http://www.wikidata.org/entity/'
        self.WD = Namespace(self.WD_uri)
        self.WDT = Namespace('http://www.wikidata.org/prop/direct/')
        self.RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
        self.DDIS = Namespace('http://ddis.ch/atai/')

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
        print("RecommenderService initialized")

    def top_match(self, entities):
        entity = entities[0]
        entity_label = entity[0]
        entity_candidates = [self.WD[e] for e in entity[2]['primary']]
        entity_candidates_secondary = [self.WD[e] for e in entity[2]['secondary']]

        targets = []
        for e in entity_candidates:
            ent = self.ent2id[e]
            # we compare the embedding of the query entity to all other entity embeddings
            dist = pairwise_distances(self.entity_emb[ent].reshape(1, -1), self.entity_emb).reshape(-1)
            # order by plausibility
            most_likely = dist.argsort()
            top_match = [
                (
                    re.sub(self.WD_uri, "wd:", self.id2ent[idx]),  # qid
                    self.ent2lbl[self.id2ent[idx]],  # label
                    dist[idx],  # score
                    rank + 1,  # rank
                )
                for rank, idx in enumerate(most_likely[:5])]
            targets += top_match

        if len(targets) == 0:
            for e in entity_candidates_secondary:
                ent = self.ent2id[e]
                # we compare the embedding of the query entity to all other entity embeddings
                dist = pairwise_distances(self.entity_emb[ent].reshape(1, -1), self.entity_emb).reshape(-1)
                # order by plausibility
                most_likely = dist.argsort()
                top_match = [
                    (
                        re.sub(self.WD_uri, "wd:", self.id2ent[idx]),  # qid
                        self.ent2lbl[self.id2ent[idx]],  # label
                        dist[idx],  # score
                        rank + 1,  # rank
                    )
                    for rank, idx in enumerate(most_likely[:5])]
                targets += top_match

        df = pd.DataFrame(targets, columns=['Target', 'TargetLabel', "Score", "Rank"])
        df = df[(df.Score != 0) & (df.TargetLabel != entity_label)].drop_duplicates().sort_values(by='Score', na_position='last').reset_index(drop=True)
        return df[:30]

    def validate_answer(self, s, p, o, o_label):
        sub = self.WD[s[len("wd:"):]]
        if re.search("ddis:", p):
            pred = self.DDIS[p[len("ddis:"):]]
        else:
            pred = self.WDT[p[len("wdt:"):]]
        obj = self.WD[o[len("wd:"):]] if re.search("wd:", o) else o

        if sub in self.ent2id and pred in self.rel2id and obj in self.ent2id:
            head = self.entity_emb[self.ent2id[sub]]
            pred = self.relation_emb[self.rel2id[pred]]
            lhs = head + pred
            dist = pairwise_distances(lhs.reshape(1, -1), self.entity_emb).reshape(-1)
            most_likely = dist.argsort()
            ranks = dist.argsort().argsort()
            if ranks[self.ent2id[obj]] > 10000:
                for rank, idx in enumerate(most_likely[:1]):
                    o = re.sub(self.WD_uri, "wd:", self.id2ent[idx])
                    o_label = self.ent2lbl[self.id2ent[idx]]
                return o, o_label,
            else:
                return o, o_label
        else:
            return o, o_label

    def find_type(self, ent):
        if ent in self.ent2id:
            head = self.entity_emb[self.ent2id[ent]]
            pred = self.relation_emb[self.rel2id[self.DDIS['indirectSubclassOf']]]
            lhs = head + pred
            dist = pairwise_distances(lhs.reshape(1, -1), self.entity_emb).reshape(-1)
            most_likely = dist.argsort()
            for rank, idx in enumerate(most_likely[1:2]):
                s = re.sub(self.WD_uri, "wd:", self.id2ent[idx])
                s_label = self.ent2lbl[self.id2ent[idx]]
            return s, s_label
        else:
            return None



