import os

import spacy  # version 3.0.6'

import spacy
from pandas.io.json import json_normalize

nlp = spacy.load("en_core_web_trf")
doc = nlp("What is the name of the lead actor in the movie Catch Me If You Can?")
span = doc[doc[4].left_edge.i : doc[4].right_edge.i+1]
with doc.retokenize() as retokenizer:
    retokenizer.merge(span)
for token in doc:
    print(token.text, token.head.text)