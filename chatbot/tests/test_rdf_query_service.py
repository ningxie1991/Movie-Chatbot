from chatbot.data.dataset import Dataset
from chatbot.algorithm.question_answering.question.parser import QuestionParser
from chatbot.algorithm.question_answering.question.patterns import get_relation
from chatbot.algorithm.question_answering.query.rdf_query_service import RDFQueryService

question_parser = QuestionParser()
dataset = Dataset()
rdf_query_service = RDFQueryService(dataset.graph)

question = 'What was Angelina Jolie born?'
entities = question_parser.parse(question)
first_entity = entities[0]
relation = get_relation(question, first_entity[0])
results = rdf_query_service.query_wh(entities, relation)
print(results)

# question = 'What is the name of the lead actor in the movie Catch Me If You Can?'
# relation = get_relation(question)
# entities = question_parser.parse(question)
# results = rdf_query_service.query_wh(entities, relation)
# print(results)
#
#
# question = 'Did Christopher Nolan ever work on a Batman movie?'
# relation = get_relation(question)
# entities = question_parser.parse(question)
# results = rdf_query_service.query_yesno(entities)
# print(results)
#
# question = 'I am a big fan of Steven Spielberg, could you recommend some of his action movies?'
# relation = get_relation(question)
# entities = question_parser.parse(question)
# results = rdf_query_service.query_action(entities)
# print(results)
#
# question = 'Can you recommend me some comedy movies?'
# relation = get_relation(question)
# entities = question_parser.parse(question)
# results = rdf_query_service.query_action(entities)
# print(results)
#
# question = 'Can you recommend me some comedy movies of Woody Allen?'
# relation = get_relation(question)
# entities = question_parser.parse(question)
# results = rdf_query_service.query_action(entities)
# print(results)