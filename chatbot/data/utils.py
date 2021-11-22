import json
import os

import pandas as pd
import numpy as np
import re
from rdflib import Namespace
from flair.data import Sentence
from flair.models import SequenceTagger

# load tagger
tagger = SequenceTagger.load("flair/pos-english")

WD = Namespace('http://www.wikidata.org/entity/')
WDT = Namespace('http://www.wikidata.org/prop/direct/')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = Namespace('http://schema.org/')

entity_type_map = {
    'TITLE': [WD.Q11424, WD.Q24856, WD.Q5398426, WD.Q7725310, WD.Q15416],
    'DIRECTOR': [WD.Q2526255, WD.Q3455803],
    'CHARACTER': [WD.Q95074, WD.Q15773347, WD.Q15632617],
    'ACTOR': [WD.Q33999, WD.Q10800557],
    'GENRE': [WD.Q483394]
}

entity_predicate_map = {
    'DIRECTOR': [WDT.P57],
    'CHARACTER': [WDT.P1441, WDT.P674],
    'ACTOR': [WDT.P161, WDT.P175],
    'GENRE': [WDT.P136]
}
        
def pos_tag(tokens):
    s = ' '.join(tokens)
    sentence = Sentence(s)
    # predict POS tags
    tagger.predict(sentence)
    pos_tags = [span.tag for span in sentence.get_spans('pos')]
    return list(zip(tokens, pos_tags))


def read_data(corpus_file):
    list_of_tags = ['B-ACTOR', 'I-ACTOR', 'B-TITLE', 'I-TITLE', 'B-CHARACTER', 'I-CHARACTER', 'B-DIRECTOR',
                    'I-DIRECTOR']
    with open(corpus_file, encoding='utf-8') as f:
        data = np.empty((0, 4))
        words = []
        words_for_pos = []
        tags = []
        sentences = []
        count = 1
        for line in f:
            line = line.strip()
            if not line:
                s = np.array(sentences).reshape((-1, 1))
                # capitalized first letter of first word
                words_for_pos[0] = words_for_pos[0].title()
                print(words)
                w = np.array(words).reshape((-1, 1))

                pos_tags = [pos for token, pos in pos_tag(words_for_pos)]
                print(pos_tags)
                p = np.array(pos_tags).reshape((-1, 1))
                t = np.array(tags).reshape((-1, 1))
                chunk = np.hstack((s, w, p, t))
                data = np.vstack((data, chunk))

                words = []
                words_for_pos = []
                tags = []
                sentences = []
                count = count + 1
            else:
                columns = line.split()
                tag = columns[0]
                word = columns[-1]
                tags.append(tag)
                if tag in list_of_tags:
                    # capitalize all names and titles
                    words_for_pos.append(word.upper())
                else:
                    words_for_pos.append(word)
                words.append(word)
                sentences.append("Sentence: " + str(count))
        return pd.DataFrame(data, columns=['Sentence #', 'Word', 'POS', 'Tag'])


def expand_property_labels(graph_properties, wikidata_properties):
    data = []
    for row in graph_properties:
        property_uri = row.p
        print(property_uri)
        if property_uri.startswith('http://www.wikidata.org/prop/direct/'):
            entity_uri = re.sub("http://www.wikidata.org/prop/direct/", "http://www.wikidata.org/entity/", property_uri)
            property_label = \
            wikidata_properties.loc[wikidata_properties['property'] == entity_uri, 'propertyLabel'].values[0]
            property_alt_label = \
            wikidata_properties.loc[wikidata_properties['property'] == entity_uri, 'propertyAltLabel'].values[0]

            all_labels_text = property_label + ', '
            if property_alt_label:
                all_labels_text + property_alt_label

            all_labels = re.split(', | or ', all_labels_text)
            for label in all_labels:
                data.append([property_uri, label])

    return pd.DataFrame(data, columns=['Property', 'PropertyLabel'])


def get_movies(graph):
    entities = []
    nodes = [s for t in entity_type_map['TITLE'] for s in graph.subjects(WDT.P31, t) if graph.value(s, RDFS.label)]

    for s in nodes:
        entities.append((s.toPython()[len(WD):], graph.value(s, RDFS.label)))

    df = pd.DataFrame(entities, columns=['Entity', 'EntityLabel'])
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def get_actors(graph):
    entities = []
    nodes = [s for pred in entity_predicate_map['ACTOR'] for s in graph.objects(None, pred) if graph.value(s, RDFS.label)]

    for s in nodes:
        entities.append((s.toPython()[len(WD):], graph.value(s, RDFS.label)))

    df = pd.DataFrame(entities, columns=['Entity', 'EntityLabel'])
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def get_directors(graph):
    entities = []
    nodes = [s for s in graph.objects(None, WDT.P57) if graph.value(s, RDFS.label)]

    for s in nodes:
        entities.append((s.toPython()[len(WD):], graph.value(s, RDFS.label)))

    df = pd.DataFrame(entities, columns=['Entity', 'EntityLabel'])
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def get_characters(graph):
    entities = []
    nodes = [s for s in graph.subjects(WDT.P175, None) if graph.value(s, RDFS.label)]
    characters = [(s, p, o) for n in nodes for t in entity_type_map['CHARACTER'] for s, p, o in
                  graph.triples((n, WDT.P31, t))]

    for s, p, o in characters:
        entities.append((s.toPython()[len(WD):], graph.value(s, RDFS.label)))

    df = pd.DataFrame(entities, columns=['Entity', 'EntityLabel'])
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def get_genres(graph):
    entities = []
    nodes = [s for s in graph.objects(None, WDT.P136) if graph.value(s, RDFS.label)]

    for s in nodes:
        entities.append((s.toPython()[len(WD):], graph.value(s, RDFS.label)))

    df = pd.DataFrame(entities, columns=['Entity', 'EntityLabel'])
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def convert_images_json():
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, '../../data/ddis/images.json'), 'r') as json_file:
        images_map = json.load(json_file)

    new_map = {}
    for item in images_map:
        for movie_id in item['movie']:
            if movie_id not in new_map:
                new_map[movie_id] = []
            new_map[movie_id].append({'img': item['img'], 'type': item['type'], 'cast': item['cast']})
        for actor_id in item['cast']:
            if actor_id not in new_map:
                new_map[actor_id] = []
            new_map[actor_id].append({'img': item['img'], 'type': item['type'], 'movie': item['movie']})

    with open(os.path.join(dirname, '../../data/ddis/new_images.json'), 'w', encoding='utf-8') as f:
        json.dump(new_map, f, ensure_ascii=False, indent=4)