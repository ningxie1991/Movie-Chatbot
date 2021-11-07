import re
from chatbot.question_answering.question.patterns import wh_pattern

# test wh_pattern
wh_questions = ['Who is the director of the Batman movie?',
                'What is the name of the lead actor in the movie Batman?']

for q in wh_questions:
    entity = "Batman"
    pattern = wh_pattern.format(entity)
    relation = re.match(pattern, q).groups()
    print("\n------- Sentence: {}\n".format(q))
    print("\n-- relation: {}\n".format(relation[0]))
    # top_match = predicate_matcher.top_match(relation[0])
    # print("\n-- top match: {}\n".format(top_match))


