from chatbot.data.dataset import Dataset
from chatbot.algorithm.question_answering.question.parser import QuestionParser
from chatbot.algorithm.question_answering.question.patterns import get_relation
from chatbot.algorithm.question_answering.service.recommender import RecommenderService

question_parser = QuestionParser()
dataset = Dataset()
recommender = RecommenderService(dataset.graph)

question = 'I like the Jurassic Park movie; can you recommend any similar movies?'
entities = question_parser.parse(question)
first_entity = entities[0]
relation = get_relation(question, first_entity[0])
results = recommender.top_match(entities)
print(results)