import re

import numpy as np
import pandas as pd
import rdflib
import spacy
from rdflib import Namespace
from spacy.kb import KnowledgeBase

import os
import csv

dirname = os.path.dirname(__file__)
entity_emb = np.load(os.path.join(dirname, '../../data/ddis/entity_embeds.npy'))
with open('../../data/ddis/entity_ids.del', 'r') as ifile:
    ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
    id2ent = {v: k for k, v in ent2id.items()}

WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = Namespace('http://www.wikidata.org/prop/direct/')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = Namespace('http://schema.org/')


def create_kb():
    """ Step 1: create the Knowledge Base in spaCy and write it to file """
    nlp = spacy.load("en_core_web_lg")
    entities = pd.read_csv(os.path.join(dirname, '../../data/ddis/14_graph_entities.csv'), encoding='utf-8')
    print(f'names: {entities.shape[0]}')

    kb = KnowledgeBase(vocab=nlp.vocab, entity_vector_length=256)
    for index, row in entities.iterrows():
        qid = row['QID']
        name = row['Name']
        vector = entity_emb[ent2id[WD[qid]]]
        print(f'qid: {qid}, name: {name}')
        kb.add_entity(entity=qid, entity_vector=vector, freq=342)  # 342 is an arbitrary value here

    for name in entities['Name']:
        if name not in kb.get_alias_strings():
            contains = entities[entities['Name'].str.contains(re.escape(name))]
            same_name_qids = contains.loc[contains['Name'] == name, 'QID'].values
            similar_name_qids = contains.loc[contains['Name'] != name, 'QID'].values
            same_name_count = same_name_qids.shape[0]
            similar_name_count = np.shape(similar_name_qids)[0]
            print(f'name: {name}, # of same_name_qids: {same_name_count}, # of similar_name_qids: {similar_name_count}')

            if similar_name_count > 0:
                base_prob = 0.6/(same_name_count + similar_name_count)
                same_name_probs = [(base_prob + 0.4/same_name_count) for qid in same_name_qids]
                similar_name_probs = [base_prob for qid in similar_name_qids]
                qids = np.append(same_name_qids, similar_name_qids)
                probs = same_name_probs + similar_name_probs
                kb.add_alias(alias=name, entities=qids, probabilities=probs)
            else:
                count = same_name_qids.shape[0]
                probs = [1/count for qid in same_name_qids]
                kb.add_alias(alias=name, entities=same_name_qids, probabilities=probs)

    kb.to_disk(os.path.join(dirname, '../question_answering/saved_models/spacy_kb'))
    nlp.to_disk(os.path.join(dirname, '../question_answering/saved_models/spacy_nlp'))


if __name__ == "__main__":
    create_kb()
