import os

import joblib
import numpy as np
import pandas as pd
from sklearn_crfsuite import metrics

from chatbot.algorithm.question_answering.utils.ner import sent2labels, collate, sent2features

dirname = os.path.dirname(__file__)
df_train = pd.read_csv(os.path.join(dirname, '../../data/mit_movies_corpus/cased/engtrain_cased.csv'))
df_test = pd.read_csv(os.path.join(dirname, '../../data/mit_movies_corpus/cased/engtest_cased.csv'))
test_sentences = collate(df_test)
X_test = [sent2features(s) for s in test_sentences]
y_test = [sent2labels(s) for s in test_sentences]

loaded_model = joblib.load(os.path.join(dirname, '../algorithm/saved_models/ner_best.sav'))
y_pred = loaded_model.predict(X_test)
classes = np.unique(df_train.Tag.values)
print("--- performance of the CRF model")
print(metrics.flat_classification_report(y_test, y_pred, labels=classes))