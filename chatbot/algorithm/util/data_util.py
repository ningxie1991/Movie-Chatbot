import pandas as pd
import numpy as np
import re
from rdflib import Namespace
from flair.data import Sentence
from flair.models import SequenceTagger

# load tagger
tagger = SequenceTagger.load("flair/pos-english")


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
        tags = []
        sentences = []
        count = 1
        for line in f:
            line = line.strip()
            if not line:
                s = np.array(sentences).reshape((-1, 1))
                # capitalized first letter of first word
                words[0] = words[0].title()
                w = np.array(words).reshape((-1, 1))

                pos_tags = [pos for token, pos in pos_tag(words)]
                p = np.array(pos_tags).reshape((-1, 1))
                t = np.array(tags).reshape((-1, 1))
                chunk = np.hstack((s, w, p, t))
                data = np.vstack((data, chunk))

                words = []
                tags = []
                sentences = []
                count = count + 1
            else:
                columns = line.split()
                tag = columns[0]
                word = columns[-1]
                tags.append(tag)
                if tag in list_of_tags:
                    # capitalized first letter of names and titles
                    words.append(word.title())
                else:
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


def get_entities_with_labels(graph):
    RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
    with_label = set(graph.subjects(RDFS.label, None))
    entities = []
    for node in with_label:
        entities.append((node.toPython(), graph.value(node, RDFS.label).toPython()))
    return pd.DataFrame(entities, columns=['Entity', 'Label'])
