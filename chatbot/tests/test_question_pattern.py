import re

from chatbot.algorithm.model.predicate_matcher import PredicateMatcher
from chatbot.algorithm.model.question_patterns import wh_pattern

# embeds_dir = '../../../data/wikidata/property_embeds.npy'
# properties_dir = '../../data/wikidata/graph_properties_expanded.csv'
# predicate_matcher = PredicateMatcher(properties_dir, embeds_dir)

# test wh_pattern
wh_questions = ['Who is the director of the Batman movie?',
                'What is the name of the lead actor in the movie Batman?',
                'Which is the character of the Batman movie?',
                'Where is the film location of Batman?',
                'Who is the actor for Batman?']

for q in wh_questions:
    entity = "Batman"
    pattern = wh_pattern.format(entity)
    relation = re.match(pattern, q).groups()
    print("\n------- Sentence: {}\n".format(q))
    print("\n-- relation: {}\n".format(relation[0]))
    # top_match = predicate_matcher.top_match(relation[0])
    # print("\n-- top match: {}\n".format(top_match))

