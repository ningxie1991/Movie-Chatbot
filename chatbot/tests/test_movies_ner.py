from chatbot.algorithm.movies_ner import MoviesNER

ner = MoviesNER()
ner.fit()
y_pred = ner.predict()
ner.save_model('Movies_NER.sav')

