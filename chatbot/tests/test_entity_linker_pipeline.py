import os

import spacy
from spacy.kb import KnowledgeBase

dirname = os.path.dirname(__file__)
nlp = spacy.load(os.path.join(dirname, '../question_answering/saved_models/spacy_nlp'))
kb = KnowledgeBase(vocab=nlp.vocab, entity_vector_length=256)

dirname = os.path.dirname(__file__)
kb.from_disk(os.path.join(dirname, '../question_answering/saved_models/spacy_kb'))
print(f"Candidates for 'character': {[c.entity_ for c in kb.get_alias_candidates('character')]}")

