import re

import joblib
import os
import pandas as pd
from chatbot.algorithm.util.ner_util import sent2features
from nltk import word_tokenize
from chatbot.algorithm.util.data_util import pos_tag
from nltk.tree import Tree
from nltk.chunk import conlltags2tree


class QuestionParser:
    def __init__(self):
        # model_dir = ../saved_models/Movies_NER.sav
        dir_name = os.path.dirname(__file__)
        self.loaded_model = joblib.load(os.path.join(dir_name, '../saved_models/Movies_NER.sav'))
        self.noun_pos = ['NN', 'NNP', 'NNPS', 'NNS']
        self.verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.wh_pos = ['WDT', 'WP', 'WP$', 'WRB']

    def get_entities(self, sentence):
        tokens = word_tokenize(re.sub('[,;.\?]', '', sentence))
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
        original_text = []
        for subtree in ne_tree:
            # checking for 'O' tags
            if type(subtree) == Tree:
                original_label = subtree.label()
                original_string = " ".join([token for token, pos in subtree.leaves()])
                original_text.append((original_string, original_label))
        return pd.DataFrame(original_text, columns=['Entity', 'Tag'])

    def get_nouns(self, sentence, entities):
        tokens = word_tokenize(re.sub('[,;.\?]', '', sentence))
        pos_tags = [pos for token, pos in pos_tag(tokens)]
        nouns = []
        for index, item in enumerate(pos_tags):
            token = tokens[index]
            if item in self.noun_pos and not entities['Entity'].str.contains(token).any():
                nouns.append(tokens[index])
        return nouns

    def get_verbs(self, sentence):
        tokens = word_tokenize(re.sub('[,;.\?]', '', sentence))
        pos_tags = [pos for token, pos in pos_tag(tokens)]
        verbs = []
        for index, item in enumerate(pos_tags):
            if item in self.verb_pos:
                verbs.append(tokens[index])
        return verbs

    @staticmethod
    def get_bos(sentence):
        tokens = word_tokenize(re.sub('[,;.\?]', '', sentence))
        sentence_with_pos = pos_tag(tokens)
        return pd.DataFrame([sentence_with_pos[0]], columns=['Word', 'POS'])
