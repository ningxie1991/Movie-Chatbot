from pandas import json_normalize

from chatbot.algorithm.data.dataset import Dataset
from chatbot.algorithm.model.query_matcher import QueryMatcher
from chatbot.algorithm.model.question_parser import QuestionParser
from qwikidata.sparql import return_sparql_query_results

# dataset = Dataset()
# graph = dataset.get_graph()
question_parser = QuestionParser()
query_matcher = QueryMatcher()

sentences = [
             # 'Who is the director of the Batman movie?',
             # 'What is the name of the lead actor in the movie Catch Me If You Can?',
              'Which is the main character of the Avengers movie?',
             # 'Who is the lead actor in Catch Me If You Can?',
             # 'Where is the film location of the Iron Man movie?',
             # 'Who is the actor of the character Tony Stark?'
             # 'Which character did Robert Downy Jr play in the Avengers movie?',
             # 'What movies star Robert Downey Jr?',
             # 'Which actor plays Tony Stark in Iron Man?',
             # 'What movies are directed by Tim Burton?'
            ]

for sentence in sentences:

    print("\n------- Sentence: {}".format(sentence))
    print("\n-- Found entities: \n")
    entities = question_parser.get_entities(sentence)
    print(entities)

    bos = question_parser.get_bos(sentence)
    print("\n-- BOS: \n")
    print(bos)

    query = query_matcher.match(sentence, entities, bos)
    print("\n-- Matched query: \n")
    print(query)

    # for row in graph.query(query):
    #     print("\n-- result: {}".format(row['lbl']))

    res = return_sparql_query_results(query)
    data = res['results']['bindings']
    df = json_normalize(data, max_level=1)
    # print(df['targetLabel.value'])
    print(df[['characterLabel.value', 'actorLabel.value']])


