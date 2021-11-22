import re
import joblib
import os

import pandas as pd
import spacy
from nltk.tokenize.treebank import TreebankWordDetokenizer
from spacy.kb import KnowledgeBase

from chatbot.algorithm.predicate_linker import PredicateLinker
from chatbot.algorithm.question_answering.utils.ner import sent2features
from nltk import word_tokenize
from chatbot.data.utils import pos_tag
from nltk.tree import Tree
from nltk.chunk import conlltags2tree


class QuestionParser:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.loaded_model = joblib.load(os.path.join(dirname, '../../saved_models/ner_best.sav'))
        self.predicate_linker = PredicateLinker()
        self.noun_pos = ['NN', 'NNP', 'NNPS', 'NNS']
        self.verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.wh_pos = ['WDT', 'WP', 'WP$', 'WRB']
        self.nlp = spacy.load(os.path.join(dirname, '../../saved_models/spacy_nlp'))
        self.kb = KnowledgeBase(vocab=self.nlp.vocab, entity_vector_length=256)
        self.kb.from_disk(os.path.join(dirname, '../../saved_models/spacy_kb'))
        self.movies = pd.read_csv(os.path.join(dirname, '../../../../data/ddis/entity_categories/movie_entities.csv'))
        self.directors = pd.read_csv(os.path.join(dirname, '../../../../data/ddis/entity_categories/director_entities.csv'))
        self.actors = pd.read_csv(os.path.join(dirname, '../../../../data/ddis/entity_categories/actor_entities.csv'))
        self.characters = pd.read_csv(os.path.join(dirname, '../../../../data/ddis/entity_categories/character_entities.csv'))
        self.genres = pd.read_csv(os.path.join(dirname, '../../../../data/ddis/entity_categories/genre_entities.csv'))

    def parse(self, sentence):
        tokens = word_tokenize(sentence)
        sentence_with_pos = pos_tag(tokens)
        test = [sent2features(sentence_with_pos)]
        pred = self.loaded_model.predict(test)
        tags = pred[0]

        # tag each token with pos
        pos_tags = [pos for token, pos in sentence_with_pos]
        # convert the BIO / IOB tags to tree
        conlltags = [(token, pos, tg) for token, pos, tg in zip(tokens, pos_tags, tags)]
        ne_tree = conlltags2tree(conlltags)
        # parse the tree to get our original text
        entities = []
        for subtree in ne_tree:
            # checking for 'O' tags
            if type(subtree) == Tree:
                original_string = TreebankWordDetokenizer().detokenize([token for token, pos in subtree.leaves()])
                original_string_clean = re.sub('[,;.\?]', '', original_string)
                original_string_alt = re.sub(' ', '-', original_string_clean)
                original_label = subtree.label()

                c_1 = [c.entity_ for c in self.kb.get_alias_candidates(original_string)]
                c_2 = [c.entity_ for c in self.kb.get_alias_candidates(original_string_clean)]
                c_3 = [c.entity_ for c in self.kb.get_alias_candidates(original_string_alt)]
                candidates = c_1 + c_2 + c_3

                if len(candidates) == 0 and original_label == 'GENRE' and not re.search("movie|film", original_string_clean):
                    original_string_clean += ' film'
                    candidates = [c.entity_ for c in self.kb.get_alias_candidates(original_string_clean)]

                # TODO: Disambiguous method should be based on whether we can find the name in the categories of entities!
                if re.search(f"(movie|film) {original_string}|{original_string} (movie|film)", sentence) and (original_label == 'CHARACTER' or original_label == 'DIRECTOR'):
                    original_label = 'TITLE'
                elif re.search(f"character {original_string}|{original_string} character", sentence) and (original_label == 'TITLE' or original_label == 'DIRECTOR'):
                    original_label = 'CHARACTER'

                entities.append((original_string, original_label, candidates))
        # print([(s, l) for s, l, c in entities])
        # print(entities)
        return entities



