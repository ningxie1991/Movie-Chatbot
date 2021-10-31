from chatbot.algorithm.model.question_parser import QuestionParser

question_parser = QuestionParser('../algorithm/saved_models/Movies_NER.sav')
entities = question_parser.get_entities('Who is the director of the Batman movie?')

print(question_parser.sentence)
print(question_parser.tokens)
print(question_parser.pos)
print(question_parser.tags)

print(entities)

noun_pos = ['NN', 'NNP', 'NNPS', 'NNS']
verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

nouns = []
verbs = []
for index, item in enumerate(question_parser.pos):
    if item in noun_pos and question_parser.tags[index] == 'O':
        nouns.append(question_parser.tokens[index])

    if item in verb_pos:
        verbs.append(question_parser.tokens[index])

print(nouns)
print(verbs)