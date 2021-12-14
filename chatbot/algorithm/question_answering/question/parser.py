import re
import contractions
import joblib
import os
from nltk.tokenize.treebank import TreebankWordDetokenizer
from chatbot.algorithm.entity_linker import EntityLinker
from chatbot.algorithm.question_answering.question.patterns import QuestionPattern
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
        self.question_pattern = QuestionPattern()
        print("QuestionParser initialized")

    def parse(self, sentence):
        sentence = contractions.fix(sentence)
        entities = self.ner(sentence)
        if entities and len(entities) > 0:
            first_entity = entities[0]
            question_type, matching_groups = self.question_pattern.categorize_question_type(sentence, True, first_entity[0])
            relation = matching_groups[0] if matching_groups and len(matching_groups) > 0 else None
        else:
            # TODO - if no entities are found, should fall back to using regex to find the entities by position
            question_type, matching_groups = self.question_pattern.categorize_question_type(sentence, False, None)
            entities = [] if question_type == "unknown" else self.ner_by_regex(sentence, matching_groups)
            relation = matching_groups[0] if matching_groups and len(matching_groups) > 0 else None

        if relation and self.question_pattern.is_embedding_questions(relation):
            question_type = "embedding"
        elif self.question_pattern.is_multi_media_question(sentence):
            question_type = "media"

        return question_type, entities, relation

    def ner(self, sentence):
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
                original_label = subtree.label()
                entity_with_candidates = self.get_candidates(sentence, original_string, original_label)
                entities.append(entity_with_candidates)
        # print(entities)
        return entities

    def get_candidates(self, sentence, original_string, original_label):
        original_string_clean = re.sub('[,;.\?]', '', original_string.strip())
        original_string_hyphen = re.sub(' ', '-', original_string_clean)
        original_string_alt = original_string + '.'

        if original_label == 'GENRE' and not re.search("movie|film", original_string_clean):
            original_string_clean += ' film'

        # Disambiguation of entity type/label
        label = self.entity_linker.disambiguation(original_string_clean, original_label) if original_label != "UNKNOWN" else original_label
        if re.search(f"(movie|film) {original_string}|{original_string} (movie|film)", sentence) and (
                label == 'CHARACTER' or label == 'DIRECTOR'):
            label = 'TITLE'
        elif re.search(f"character {original_string}|{original_string} character", sentence) and (
                label == 'TITLE' or label == 'DIRECTOR'):
            label = 'CHARACTER'

        c_1_primary, c_1_secondary = self.entity_linker.get_candidates(original_string)
        c_2_primary, c_2_secondary = self.entity_linker.get_candidates(original_string_clean)
        c_3_primary, c_3_secondary = self.entity_linker.get_candidates(original_string_hyphen)
        c_4_primary, c_4_secondary = self.entity_linker.get_candidates(original_string_alt)
        c_primary = c_1_primary + c_2_primary + c_3_primary + c_4_primary
        c_secondary = c_1_secondary + c_2_secondary + c_3_secondary + c_4_secondary

        # remove duplicates
        primary_candidates = list(set(c_primary))
        secondary_candidates = list(set(c_secondary) - set(c_primary))
        return original_string, label, {"primary": primary_candidates, "secondary": secondary_candidates}

    def ner_by_regex(self, sentence, matching_groups):
        entities = []
        if matching_groups and len(matching_groups) > 0:
            for group in matching_groups[1:]:
                if group:
                    # TODO: differentiate entities and relations
                    entities.append(self.get_candidates(sentence, group.strip(), "UNKNOWN"))

        return entities




