import os

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics import pairwise_distances


class PredicateLinker:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
        # properties_dir = ../../../data/wikidata/graph_properties_expanded.csv
        # embeds_dir = ../../..//data/wikidata/property_embeds.npy
        dirname = os.path.dirname(__file__)
        self.properties = pd.read_csv(os.path.join(dirname, '../../data/wikidata/graph_properties_expanded.csv'))
        self.property_labels = self.properties['PropertyLabel']
        self.property_embeds = np.load(os.path.join(dirname, '../../data/wikidata/property_embeds.npy'))

    def top_match(self, relation):
        relation_embed = self.model.encode(relation)
        dist = pairwise_distances(relation_embed.reshape(1, -1), self.property_embeds).reshape(-1)
        most_likely = dist.argsort()
        top_match = [
            (
                self.properties.loc[self.properties['PropertyLabel'] == self.property_labels[idx], 'Property'].values[0],
                self.property_labels[idx],  # label
                dist[idx],  # score
                rank + 1,  # rank
            )
            for rank, idx in enumerate(most_likely[:3])]
        return top_match
