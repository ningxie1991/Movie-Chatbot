import os
import re

import numpy as np
import pandas as pd
from rdflib import URIRef, Namespace
from sentence_transformers import SentenceTransformer

from chatbot.data.dataset import Dataset
from chatbot.data.utils import read_data, expand_property_labels, get_movies, \
    get_directors, get_actors, get_characters, get_genres, convert_images_json

dirname = os.path.dirname(__file__)

def process_mit_movies_data():
    train = read_data(os.path.join(dirname, '../../../data/mit_movies_corpus/engtrain.bio'))
    train.to_csv(os.path.join(dirname, "../../../data/mit_movies_corpus/engtrain_v2.csv"), index=False)

    test = read_data(os.path.join(dirname, '../../../data/mit_movies_corpus/engtest.bio'))
    test.to_csv(os.path.join(dirname, "../../../data/mit_movies_corpus/engtest_v2.csv"), index=False)


def map_wikidata_properties(graph_dir):
    dataset = Dataset(graph_dir)
    graph = dataset.get_graph()
    print("Parsed graph")

    # get all the distinct wikidata properties from the graph
    graph_properties = graph.query('''
        PREFIX ns1: <http://www.wikidata.org/prop/direct/>

        SELECT DISTINCT ?p WHERE {
            ?s ?p ?o
            FILTER( STRSTARTS(str(?p), str(ns1:)) )
        }
        '''
                                   )

    # pre-saved all the properties and their labels from wikidata
    wikidata_properties = pd.read_csv('../../data/wikidata/properties.csv')
    df = expand_property_labels(graph_properties, wikidata_properties)
    df.to_csv("../../data/wikidata/graph_properties_expanded.csv", index=False)


def movie_entities(graph):

    df = get_movies(graph)
    df.to_csv("../../data/ddis/movie_entities.csv", index=False)


def director_entities(graph):
    df = get_directors(graph)
    df.to_csv("../../data/ddis/director_entities.csv", index=False)


def actor_entities(graph):
    df = get_actors(graph)
    df.to_csv("../../data/ddis/actor_entities.csv", index=False)


def character_entities(graph):
    df = get_characters(graph)
    df.to_csv("../../data/ddis/character_entities.csv", index=False)


def genre_entities(graph):
    df = get_genres(graph)
    df.to_csv("../../data/ddis/genre_entities.csv", index=False)


def save_property_embeds(properties_dir, embeds_dir):
    model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
    properties = pd.read_csv(properties_dir)
    property_labels = properties['PropertyLabel']
    property_embeds = model.encode(property_labels)
    np.save(embeds_dir, property_embeds)


def save_entity_embeds(entities_dir, embeds_dir):
    model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
    entities = pd.read_csv(entities_dir)
    entity_labels = entities['Label']
    entity_embeds = model.encode(entity_labels)
    np.save(embeds_dir, entity_embeds)


def save_embeds(graph, query, embeds_dir):
    model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
    labels = []
    for row in graph.query(query):
        labels.append(row['lbl'].toPython())
    df = pd.DataFrame(labels, columns=['Label'])
    df['Label']
    movie_embeds = model.encode(df['Label'])
    np.save(embeds_dir, movie_embeds)


if __name__ == "__main__":
    convert_images_json()
