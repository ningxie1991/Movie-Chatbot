import os
import warnings

import spacy
import srsly
from spacy.tokens import DocBin

dirname = os.path.dirname(__file__)


def convert_data():
    nlp = spacy.blank("en")
    training_data = srsly.read_json(os.path.join(dirname, '../data/engtest_cased.json'))
    # the DocBin will store the example documents
    db = DocBin()
    for text, annotations in training_data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(os.path.join(dirname, "../data/dev.spacy"))


convert_data()

