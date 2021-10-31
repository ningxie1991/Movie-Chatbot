from chatbot.algorithm.question_parser import QuestionParser

question_parser = QuestionParser('../algorithm/saved_models/Movies_NER.sav')
entities = question_parser.get_entities('Who is the director of the Batman movie?')

print(question_parser.sentence)
print(question_parser.tokens)
print(question_parser.pos)
print(question_parser.tags)

print(entities)