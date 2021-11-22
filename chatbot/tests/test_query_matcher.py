from chatbot.sparql_module.question_answering.question.parser import QuestionParser
from chatbot.sparql_module.question_answering.question.patterns import get_relation

question_parser = QuestionParser()

# print("\n------- Sentence: {}".format('Who is the actor of the character Thor?'))
# entities = question_parser.parse('Who is the director of the Batman movie?')
# query = question_parser.query_wh('Who is the director of the Batman movie?', entities)
# # Who is the actor of the character Iron Man?

# print("\n------- Sentence: {}".format('Did Christopher Nolan ever work on a Batman movie?'))
# entities, bos = question_parser.parse('Did Christopher Nolan ever work on a Batman movie?')
# query = question_parser.query_yesno(entities)

# 'I like the Jurassic Park movie; can you recommend any similar movies?'
# 'I am a big fan of Steven Spielberg, could you recommend some of his action movies?'

question = 'I am a big fan of Steven Spielberg, could you recommend some of his action movies?'
relation = get_relation(question)
entities = question_parser.parse(question)
query = question_parser.query_action(entities, relation)


