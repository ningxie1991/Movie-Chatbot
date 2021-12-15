def collate(dataframe):
    agg_func = lambda s: [(w, p, t) for w, p, t in
                          zip(s['Word'].values.tolist(), s['POS'].values.tolist(), s['Tag'].values.tolist())]
    grouped = dataframe.groupby('Sentence #').apply(agg_func)
    return [s for s in grouped]


def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'word.lower()': word.lower(),  # the word in lowercase
        'word[-3:]': word[-3:],  # last three characters
        'word[-2:]': word[-2:],  # last two characters
        'word.isupper()': word.isupper(),  # true, if the word is in uppercase
        'word.istitle()': word.istitle(),
        # true, if the first character is in uppercase and remaining characters are in lowercase
        'word.isdigit()': word.isdigit(),  # true, if all characters are digits
        'postag': postag,  # POS tag
        'postag[:2]': postag[:2],  # IOB prefix
    }
    if i > 0:
        word1 = sent[i - 1][0]  # the previous word
        postag1 = sent[i - 1][1]  # POS tag of the previous word
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })  # add some features of the previous word
    else:
        features['BOS'] = True  # BOS: begining of the sentence

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]  # the next word
        postag1 = sent[i + 1][1]  # POS tag of the next word
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })  # add some features of the next word
    else:
        features['EOS'] = True  # EOS: end of the sentence
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]