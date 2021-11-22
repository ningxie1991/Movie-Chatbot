import os

import joblib
import numpy as np
import pandas as pd
import sklearn_crfsuite
from chatbot.algorithm.question_answering.utils.ner import collate, sent2features, sent2labels


class MoviesNER:
    def __init__(self):
        # train_cased = /data/mit_movies_corpus/engtrain_cased.csv
        # test_cased = /data/mit_movies_corpus/engtest_cased.csv
        # train= /data/mit_movies_corpus/engtrain.csv
        # test = /data/mit_movies_corpus/engtest.csv
        dirname = os.path.dirname(__file__)
        self.df_train = pd.read_csv(os.path.join(dirname, '../../../data/mit_movies_corpus/engtrain.csv'))
        self.df_test = pd.read_csv(os.path.join(dirname, '../../../data/mit_movies_corpus/engtest.csv'))
        self.crf = sklearn_crfsuite.CRF(
            algorithm='l2sgd',  # l2sgd: Stochastic Gradient Descent with L2 regularization term
            max_iterations=1000,  # maximum number of iterations
        )
        self.classes = np.unique(self.df_train.Tag.values)
        train_sentences = collate(self.df_train)
        test_sentences = collate(self.df_test)
        self.X_train = [sent2features(s) for s in train_sentences]
        self.y_train = [sent2labels(s) for s in train_sentences]
        self.X_test = [sent2features(s) for s in test_sentences]
        self.y_test = [sent2labels(s) for s in test_sentences]

    def fit(self):
        self.crf.fit(self.X_train, self.y_train)

    def predict(self):
        y_pred = self.crf.predict(self.X_test)
        return y_pred

    def save_model(self, relative_file_path):
        dir_name = os.path.dirname(__file__)
        file_name = os.path.join(dir_name, relative_file_path)
        joblib.dump(self.crf, file_name)


if __name__ == "__main__":
    ner = MoviesNER()
    ner.fit()
    ner.save_model('./output/ner_best.sav')