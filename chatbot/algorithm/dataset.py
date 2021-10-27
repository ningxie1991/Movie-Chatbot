from rdflib.namespace import Namespace, RDF, RDFS, XSD
import rdflib
import numpy as np

entity_emb = np.load('../../data/entity_embeds.npy')
relation_emb = np.load('../../data/relation_embeds.npy')