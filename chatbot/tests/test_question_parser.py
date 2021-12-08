from chatbot.algorithm.question_answering.question.parser import QuestionParser

question_parser = QuestionParser()
sentences = [ "I like Finding Nemo; can you recommend some similar movies?",
             "Who's the director of the Batman movie?",
             # 'Did Christopher Nolan ever work on a Batman movie?',
             # 'Who is the director of the Batman movie?',
             # 'What is the name of the lead actor in the movie Catch Me If You Can?',
             # 'Who is the lead actor in Catch Me If You Can?',
             # 'which is the main character of the avengers movie?',
             # 'Where is the film location of the Iron Man movie?',
             # 'What is the character of Robert Downey Jr. in the Avengers movie?',
             # 'Which character did Robert Downy Jr play in the Avengers movie?',
             'What movies star Robert Downey Jr?',
             'Which actor plays Tony Stark in Iron Man?',
             # 'What movies are directed by Tim Burton?']
             # 'Did Christopher Nolan ever work on a Batman movie?',
             'I like the Jurassic Park movie; can you recommend any similar movies?',
             'I am a big fan of Steven Spielberg, could you recommend some of his action movies?',
             # 'Show me the pictures of the lead actors of the movie Jurassic Park.',
             # 'Can you show me the poster of the movie Batman?',
             # 'Show me an action movie poster.'
]

for sentence in sentences:
    print(f"\n------- Sentence: {sentence}")
    entities = question_parser.parse(sentence)
    print(f"--- entities: {entities}\n")



