import re
from chatbot.algorithm.model.predicate_matcher import PredicateMatcher
from chatbot.algorithm.model.query_templates import QuestionTemplates
from chatbot.algorithm.model.question_patterns import wh_pattern, main_actor_character_pattern


class QueryMatcher:
    def __init__(self):
        self.query_templates = QuestionTemplates()
        self.wh_pos = ['WDT', 'WP', 'WP$', 'WRB']
        self.predicate_matcher = PredicateMatcher()

    def match(self, sentence, entities, bos):
        query = ''
        # if it's a wh-question and there's only one entity found
        if bos['POS'].iloc[0] in self.wh_pos and entities.shape[0] == 1:
            entity_label = entities['Entity'].iloc[0]
            entity_type = entities['Tag'].iloc[0]
            pattern = wh_pattern.format(entity_label)
            relation = re.match(pattern, sentence).groups()[0]
            print("\n---- relation: {}".format(relation))

            if entity_type == 'TITLE' and re.search(main_actor_character_pattern, relation):
                query = self.query_templates.main_actor_character_query(entity_label)
            else:
                matched_pred = self.predicate_matcher.top_match(relation)
                print("\n---- matched pred: {}".format(matched_pred))
                if entity_type == 'CHARACTER' and matched_pred['Label'] == 'actor':
                    # different predicate because 'actor' will always match wdt:P161 which is cast member
                    # in this case, we want the wdt:P175 which is performer
                    pred = 'wdt:P175'
                else:
                    pred = matched_pred['Entity']
                # query = self.query_templates.generate_query(entity_label, matched_pred)
                query = self.query_templates.generate_wiki_query(entity_label, pred)
        return query

