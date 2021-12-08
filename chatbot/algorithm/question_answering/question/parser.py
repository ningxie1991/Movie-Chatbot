import re
import contractions
import joblib
import os
from nltk.tokenize.treebank import TreebankWordDetokenizer
from chatbot.algorithm.entity_linker import EntityLinker
from chatbot.algorithm.question_answering.utils.ner import sent2features
from nltk import word_tokenize
from chatbot.data.utils import pos_tag
from nltk.tree import Tree
from nltk.chunk import conlltags2tree


class QuestionParser:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.loaded_model = joblib.load(os.path.join(dirname, '../../saved_models/ner_best.sav'))
        self.entity_linker = EntityLinker()
        print("QuestionParser initialized")

    def parse(self, sentence):
        sentence = contractions.fix(sentence)
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
                original_string_hyphen = re.sub(' ', '-', original_string_clean)
                original_string_alt = original_string + '.'
                original_label = subtree.label()

                # Disambiguation of entity type/label
                label = self.entity_linker.disambiguation(original_string_clean, original_label)
                if re.search(f"(movie|film) {original_string}|{original_string} (movie|film)", sentence) and (label == 'CHARACTER' or label == 'DIRECTOR'):
                    label = 'TITLE'
                elif re.search(f"character {original_string}|{original_string} character", sentence) and (label == 'TITLE' or label == 'DIRECTOR'):
                    label = 'CHARACTER'

                c_1 = self.entity_linker.get_candidates(original_string, label)
                c_2 = self.entity_linker.get_candidates(original_string_clean, label)
                c_3 = self.entity_linker.get_candidates(original_string_hyphen, label)
                c_4 = self.entity_linker.get_candidates(original_string_alt, label)
                c = c_1 + c_2 + c_3 + c_4
                # remove duplicates
                candidates = list(set(c))

                if len(candidates) == 0 and label == 'GENRE' and not re.search("movie|film", original_string_clean):
                    original_string_clean += ' film'
                    candidates = self.entity_linker.get_candidates(original_string_clean, label)

                entities.append((original_string, label, candidates))
        # print(entities)
        return entities





