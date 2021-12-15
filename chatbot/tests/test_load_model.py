import os
import joblib
from chatbot.algorithm.question_answering.utils.ner import sent2features

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../algorithm/my_entity_recognizer/output/ner_best.sav')
loaded_model = joblib.load(filename)

test_sentence_1 = [['Who', 'WP'], ['is', 'VBZ'],['the', 'DT'],['director', 'NN'],['of', 'IN'],['the', 'DT'],["Batman", 'NNP'],['movie', 'NN']]
test_sentence_2 = [['Who', 'WP'], ['is', 'VBZ'], ['the', 'DT'], ['main', 'JJ'], ['character', 'NN'], ['in', 'IN'], ['the', 'DT'], ['movie', 'NN'], ['Catch', 'VB'], ['Me', 'PRP'], ['If', 'IN'], ['You', 'PRP'], ['Can', 'MD']]
test_sentence_3 = [('Did', 'VBD'), ('Christopher', 'NNP'), ('Nolan', 'NNP'), ('ever', 'RB'), ('work', 'VB'), ('on', 'IN'), ('a', 'DT'), ('Batman', 'NNP'), ('movie', 'NN')]
test_sentence_4= [('I', 'PRP'), ('am', 'VBP'), ('a', 'DT'), ('big', 'JJ'), ('fan', 'NN'), ('of', 'IN'), ('Steven', 'NNP'), ('Spielberg,', 'NNP'), ('could', ','), ('you', 'MD'), ('recommend', 'PRP'), ('some', 'VB'), ('of', 'DT'), ('his', 'IN'), ('action', 'PRP$'), ('movies', 'NN')]

test = [sent2features(test_sentence_3)]
pred = loaded_model.predict(test)

print(pred)