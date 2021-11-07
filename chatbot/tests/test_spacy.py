import os

import spacy  # version 3.0.6'

# initialize language model
nlp = spacy.load("en_core_web_md")

kb = spacy.KBFromFile.v1(os.path.abspath(__file__ + '/../../../data_spacy_entity_linker/wikidb_filtered.db'))

# add pipeline (declared through entry_points in setup.py)
nlp.add_pipe("entityLinker", last=True)

doc = nlp("What is the name of the lead actor of the movie Catch Me If You Can?")

# returns all entities in the whole document
all_linked_entities = doc._.linkedEntities
# iterates over sentences and prints linked entities
for sent in doc.sents:
    sent._.linkedEntities.pretty_print()

# OUTPUT:
# https://www.wikidata.org/wiki/Q194318     Pirates of the Caribbean        Series of fantasy adventure films
# https://www.wikidata.org/wiki/Q12525597   Silvester                       the day celebrated on 31 December (Roman Catholic Church) or 2 January (Eastern Orthodox Churches)

