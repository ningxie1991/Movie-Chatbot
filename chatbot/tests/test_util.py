import re

from nltk import word_tokenize
from chatbot.algorithm.util.data_util import pos_tag

sentence = "Show me an action movie poster."
tokens = word_tokenize(re.sub('[,;.\?]', '', sentence))
sentence_with_pos = pos_tag(tokens)
print(sentence_with_pos)

