import re
import joblib
import os
import spacy
from nltk.tokenize.treebank import TreebankWordDetokenizer
from spacy.kb import KnowledgeBase

from chatbot.data.dataset import Dataset
from chatbot.my_entity_linker.entity_linker import EntityLinker
from chatbot.my_predicate_linker.predicate_linker import PredicateLinker
from chatbot.question_answering.ner_utils import sent2features
from nltk import word_tokenize
from chatbot.data.utils import pos_tag
from nltk.tree import Tree
from nltk.chunk import conlltags2tree
from chatbot.question_answering.sparql_query.query_matcher import wh_query, yesno_query, action_query


class QuestionParser:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.loaded_model = joblib.load(os.path.join(dirname, '../saved_models/ner_best.sav'))
        self.predicate_linker = PredicateLinker()
        # dataset = Dataset()
        # self.entity_linker = EntityLinker(dataset.graph)
        self.noun_pos = ['NN', 'NNP', 'NNPS', 'NNS']
        self.verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.wh_pos = ['WDT', 'WP', 'WP$', 'WRB']
        self.nlp = spacy.load(os.path.join(dirname, '../saved_models/spacy_nlp'))
        self.kb = KnowledgeBase(vocab=self.nlp.vocab, entity_vector_length=256)
        self.kb.from_disk(os.path.join(dirname, '../saved_models/spacy_kb'))

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
                original_label = subtree.label()

                c_1 = [c.entity_ for c in self.kb.get_alias_candidates(original_string)]
                c_2 = [c.entity_ for c in self.kb.get_alias_candidates(original_string_clean)]
                candidates = c_1 + c_2

                if len(candidates) == 0 and original_label == 'GENRE' and not re.search("movie|film", original_string_clean):
                    original_string_clean += ' film'
                    candidates = [c.entity_ for c in self.kb.get_alias_candidates(original_string_clean)]

                if re.search(f"(movie|film) {original_string}|{original_string} (movie|film)", sentence) and original_label == 'CHARACTER':
                    original_label = 'TITLE'
                elif re.search(f"character {original_string}|{original_string} character", sentence) and original_label == 'TITLE':
                    original_label = 'CHARACTER'
                entities.append((original_string, original_label, candidates))
        print(entities)

        # nouns = []
        # verbs = []
        # for index, item in enumerate(pos_tags):
        #     token = tokens[index]
        #     if item in self.noun_pos:
        #         nouns.append(token)
        #     elif item in self.verb_pos:
        #         verbs.append(token)
        return entities

    def query_wh(self, entities, relation):
        matched_pred = self.predicate_linker.top_match(relation)
        print(f"relation: {relation}, matched_pred: {matched_pred}")
        query = wh_query(entities, relation, matched_pred[0])
        return query

    @staticmethod
    def query_yesno(entities):
        query = yesno_query(entities)
        return query

    @staticmethod
    def query_action(entities, relation):
        # matched_entity = self.entity_linker.top_match(re.sub('[,;.\?]', '', relation))
        # print(f"target_type: {target_type}, matched_entity: {matched_entity}")
        query = action_query(entities, relation)
        return query



