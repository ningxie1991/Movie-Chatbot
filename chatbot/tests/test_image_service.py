from chatbot.data.dataset import Dataset
from chatbot.algorithm.question_answering.question.parser import QuestionParser
from chatbot.algorithm.question_answering.question.patterns import get_relation
from chatbot.algorithm.question_answering.service.image import ImageService

question_parser = QuestionParser()
dataset = Dataset()
image_service = ImageService(dataset.graph)

question = 'Show me an action movie poster.'
entities = question_parser.parse(question)
first_entity = entities[0]
relation = get_relation(question, first_entity[0])
print(relation)
results = image_service.top_match(entities, relation)
print(results)