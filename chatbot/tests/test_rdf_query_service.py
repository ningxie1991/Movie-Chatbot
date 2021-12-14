from chatbot.data.dataset import Dataset
from chatbot.algorithm.question_answering.question.parser import QuestionParser
from chatbot.algorithm.question_answering.query.rdf_query_service import RDFQueryService

question_parser = QuestionParser()
dataset = Dataset()
rdf_query_service = RDFQueryService(dataset.graph)

question = 'Did Christopher Nolan ever work on a Batman movie?'
question_type, entities, relation = question_parser.parse(question)
first_entity = entities[0]
results = rdf_query_service.query_yesno(entities)
print(results)
