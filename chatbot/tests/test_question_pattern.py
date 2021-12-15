# test question patterns
from chatbot.algorithm.question_answering.question.patterns import QuestionPattern

question_pattern = QuestionPattern()
questions = [
             "Who's the director of the Batman movie?",
             'Did Christopher Nolan ever work on a Batman movie?',
             'What is the name of the lead actor in the movie Catch Me If You Can?',
             'Who is the lead actor in Catch Me If You Can?',
             'which is the main character of the Avengers movie?',
             'Where is the film location of the Iron Man movie?',
             'Where was Angelina Jolie born?',
             'What does George Clooney look like?',
             'I like the Jurassic Park movie; can you recommend any similar movies?',
             'I am a big fan of Steven Spielberg, could you recommend some of his action movies?',
             'Show me the pictures of the lead actors of the movie Jurassic Park.',
             'Can you show me the poster of the movie Batman?',
             'Show me an action movie poster.',
             "Can you recommend some actions movies directed by Steven Spielberg?",
             'What is the type of comics?',
             'What is a comics?',
             'What is the profession of Jean Von Hamme?'
]

for q in questions:
    if question_pattern.is_wh_question(q):
        match = question_pattern.is_wh_question(q).groups()
        print(f"Q: {q}, question type: wh")
        print(match)
        for m in match:
            if m:
                print(m.strip())
    elif question_pattern.is_recommender_question(q):
        match = question_pattern.is_recommender_question(q).groups()
        print(f"Q: {q}, question type: recommender")
        print(match)
        for m in match:
            if m:
                print(m.strip())
    # if is_wh_question(q):
    #     print(f"Q: {q}, question type: wh")
    # elif is_yesno_question(q):
    #     print(f"Q: {q}, question type: yesno")
    # elif is_action_question(q):
    #     print(f"Q: {q}, question type: action")
