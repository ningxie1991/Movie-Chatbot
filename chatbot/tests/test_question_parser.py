from chatbot.algorithm.model.question_parser import QuestionParser

question_parser = QuestionParser()

sentences = ['Who is the director of the Batman movie?',
             'What is the name of the lead actor in the movie Catch Me If You Can?',
             'Who is the lead actor in Catch Me If You Can?',
             'Which is the main character of the Avengers movie?',
             'Where is the film location of the Iron Man movie?',
             'Who is the actor of the character Tony Stark?',
             'Which character did Robert Downy Jr play in the Avengers movie?',
             'What movies star Robert Downey Jr?',
             'Which actor plays Tony Stark in Iron Man?',
             'What movies are directed by Tim Burton?']
             # 'Did Christopher Nolan ever work on a Batman movie?',
             # 'I like the Jurassic Park movie; can you recommend any similar movies?',
             # 'I am a big fan of Steven Spielberg, could you recommend some of his action movies?',
             # 'Show me the pictures of the lead actors of the movie Jurassic Park.',
             # 'Can you show me the poster of the movie Batman?',
             # 'Show me an action movie poster.']

for sentence in sentences:

    print("\n------- Sentence: {}".format(sentence))
    print("\n-- Found entities: \n")
    entities = question_parser.get_entities(sentence)
    print(entities)

    nouns = question_parser.get_nouns(sentence, entities)
    print("\n-- Other nouns: \n")
    print(nouns)

    # for n in nouns:
    #     top_match = predicate_matcher.top_match(n)
    #     print("\n-- top match: {}\n".format(top_match))

    verbs = question_parser.get_verbs(sentence)
    print("\n-- All verbs: \n")
    print(verbs)

    bos = question_parser.get_bos(sentence)
    print("\n-- BOS: \n")
    print(bos)

