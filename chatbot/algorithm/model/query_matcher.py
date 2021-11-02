import re
from chatbot.algorithm.model.predicate_matcher import PredicateMatcher
from chatbot.algorithm.model.query_templates import QuestionTemplates
from chatbot.algorithm.model.question_patterns import wh_pattern


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
            matched_pred = self.predicate_matcher.top_match(relation)
            print("\n---- matched pred: {}".format(matched_pred))

            if entity_type == 'TITLE':
                query = self.query_templates.title_related_query(entity_label, matched_pred)
            elif entity_type == 'DIRECTOR':
                query = self.query_templates.director_related_query(entity_label, matched_pred)
            elif entity_type == 'ACTOR':
                query = self.query_templates.actor_related_query(entity_label, matched_pred)
            elif entity_type == 'CHARACTER':
                query = self.query_templates.chracter_related_query(entity_label, matched_pred)
        return query

