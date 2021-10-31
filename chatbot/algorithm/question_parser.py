import joblib
import nltk
import os
from chatbot.algorithm.util.data_util import sentence2tokens, tag_pos
from chatbot.algorithm.util.ner_util import sent2features

nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag
from nltk.tree import Tree
from nltk.chunk import conlltags2tree


class QuestionParser:
    def __init__(self, model_file_path):
        dir_name = os.path.dirname(__file__)
        file_name = os.path.join(dir_name, model_file_path)
        self.loaded_model = joblib.load(file_name)
        self.sentence = ''
        self.tokens = []
        self.tags = []
        self.pos = []

    def get_entities(self, sentence):
        self.sentence = sentence
        self.tokens = sentence2tokens(sentence)
        self.pos = tag_pos(self.tokens)
        sentence_with_pos = list(zip(self.tokens, self.pos))
        test = [sent2features(sentence_with_pos)]
        pred = self.loaded_model.predict(test)
        self.tags = pred[0]

        # tag each token with pos
        pos_tags = [pos for token, pos in pos_tag(self.tokens)]
        # convert the BIO / IOB tags to tree
        conlltags = [(token, pos, tg) for token, pos, tg in zip(self.tokens, pos_tags, self.tags)]
        ne_tree = conlltags2tree(conlltags)
        # parse the tree to get our original text
        original_text = []
        for subtree in ne_tree:
            # checking for 'O' tags
            if type(subtree) == Tree:
                original_label = subtree.label()
                original_string = " ".join([token for token, pos in subtree.leaves()])
                original_text.append((original_string, original_label))
        return original_text
