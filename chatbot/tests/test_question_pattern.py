from chatbot.question_answering.question.patterns import is_action_question, is_wh_question, is_yesno_question

# test question patterns
questions = [
                'Who is the director of the Batman movie?',
                'What is the name of the lead actor in the movie Batman?',
                'What is the Batman movie about?',
                'Did Christopher Nolan ever work on a Batman movie?',
                'Did Robert Downey Jr. ever appear in an Avengers movie?',
                'I am a big fan of Steven Spielberg, could you recommend some of his action movies?',
                'I like the Jurassic Park movie; can you recommend any similar movies?',
                'Can you show me the poster of the movie Batman?',
                'Play me a song.',
                'Show me something interesting.',
                'Show me the pictures of the lead actors of the movie Jurassic Park.',
                'Show me an action movie poster.'
]

for q in questions:
    if is_wh_question(q):
        print(f"Q: {q}, question type: wh")
    elif is_yesno_question(q):
        print(f"Q: {q}, question type: yesno")
    elif is_action_question(q):
        print(f"Q: {q}, question type: action")
    else:
        print(f"Q: {q}, question type: UNKNOWN")