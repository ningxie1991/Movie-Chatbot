import json

import pandas as pd
import numpy as np
import re
from flair.data import Sentence
from flair.models import SequenceTagger

# load tagger
tagger = SequenceTagger.load("flair/pos-english")


def sentence2tokens(sentence_text):
    if sentence_text[-1] == '?' or sentence_text[-1] == '.':
        sentence_array = sentence_text[:-1].split(' ')
    else:
        sentence_array = sentence_text.split(' ')
    return sentence_array


def sentence2input(sentence_text):
    sentence = Sentence(sentence_text)
    # predict POS tags
    tagger.predict(sentence)
    sentence_array = sentence2tokens(sentence_text)
    tag_array = tag_pos(sentence_array)
    return list(zip(sentence_array, tag_array))


def tag_pos(sentence_array):
    s = ' '.join(sentence_array)
    sentence = Sentence(s)
    # predict POS tags
    tagger.predict(sentence)
    spans = sentence.get_spans('pos')
    return [span.tag for span in spans]


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

                pos_tags = tag_pos(words)
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


def elaborate_property_labels(graph_properties, wikidata_properties):
    data = []
    for row in graph_properties:
        property_uri = row.p
        print(property_uri)
        if property_uri.startswith('http://www.wikidata.org/prop/direct/'):
            entity_uri = re.sub("http://www.wikidata.org/prop/direct/", "http://www.wikidata.org/entity/", property_uri)
            property_label = wikidata_properties.loc[wikidata_properties['property'] == entity_uri, 'propertyLabel'].values[0]
            property_alt_label = wikidata_properties.loc[wikidata_properties['property'] == entity_uri, 'propertyAltLabel'].values[0]

            all_labels_text = property_label + ', '
            if property_alt_label:
                all_labels_text + property_alt_label

            all_labels = re.split(', | or ', all_labels_text)
            for label in all_labels:
                data.append([property_uri, label])

    return pd.DataFrame(data, columns=['Property', 'PropertyLabel'])
