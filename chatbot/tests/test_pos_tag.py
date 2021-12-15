from nltk import word_tokenize
from chatbot.data.utils import pos_tag

sentence = 'Did Christopher Nolan ever work on a Batman movie?'
tokens = word_tokenize(sentence)
pos_tagged = pos_tag(tokens)
print(pos_tagged)