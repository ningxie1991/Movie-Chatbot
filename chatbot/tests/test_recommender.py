from rdflib import Namespace

from chatbot.data.dataset import Dataset
from chatbot.algorithm.question_answering.question.parser import QuestionParser
from chatbot.algorithm.question_answering.question.patterns import get_relation
from chatbot.algorithm.question_answering.service.embedding import EmbeddingService

question_parser = QuestionParser()
dataset = Dataset()
embedding_service = EmbeddingService(dataset.graph)

# question = 'I like Iron Man; can you recommend any similar movies?'
# entities = question_parser.parse(question)
# first_entity = entities[0]
# relation = get_relation(question, first_entity[0])
# results = embedding_service.top_match(entities)
# print(results)

WD = Namespace('http://www.wikidata.org/entity/')
WDT = Namespace('http://www.wikidata.org/prop/direct/')

for s, p, o in dataset.graph.triples((WD.Q1406, WDT.P577, None)):
    embedding_service.validate_answer(s, p, o)
