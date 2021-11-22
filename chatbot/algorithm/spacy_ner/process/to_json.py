import json
import os
import re

import pandas as pd
from nltk import conlltags2tree, Tree
from nltk.tokenize.treebank import TreebankWordDetokenizer


def to_json():
    dirname = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(dirname, '../../../../data/mit_movies_corpus/cased/engtest_cased.csv'))
    grouped = df.groupby('Sentence #')
    data = []
    for name, group in grouped:
        tokens = group['Word'].values
        pos_tags = group['POS'].values
        tags = group['Tag'].values
        sentence = TreebankWordDetokenizer().detokenize(tokens)
        print(sentence)

        # convert the BIO / IOB tags to tree
        records = group.to_records(index=False)
        conlltags = [(token, pos, tg) for token, pos, tg in zip(tokens, pos_tags, tags)]
        ne_tree = conlltags2tree(conlltags)
        # parse the tree to get our original text
        entities = []
        start_index = 0
        for subtree in ne_tree:
            # checking for 'O' tags
            if type(subtree) == Tree:
                original_label = subtree.label()
                original_string = TreebankWordDetokenizer().detokenize([token for token, pos in subtree.leaves()])
                end_index = start_index + len(original_string)
                entities.append((start_index, end_index, original_label))
                start_index = end_index + 1
            else:
                start_index += len(subtree[0]) + 1
        data.append((sentence, {"entities": entities}))

    with open('../data/engtest_cased.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


to_json()