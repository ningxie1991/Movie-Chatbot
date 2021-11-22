from chatbot.speakeasy.app import App


if __name__ == "__main__":
    app = App()
    while True:
        try:
            question = input("Ask:")
            response = app.get_response(question)
        except Exception as e:
            print("Error:", e)

# questions = [
#              'Who is the director of the Batman movie?',
#              'Did Christopher Nolan ever work on a Batman movie?',
#              'What is the name of the lead actor in the movie Catch Me If You Can?',
#              'I like the Jurassic Park movie; can you recommend any similar movies?',
#              'I am a big fan of Steven Spielberg, could you recommend some of his action movies?',
#              'Show me the pictures of the lead actors of the movie Jurassic Park.',
#              'Can you show me the poster of the movie Batman?',
#              'Show me an action movie poster.'
#              ]
#
# app = App()
# for q in questions:
#     response = app.get_response(q)

