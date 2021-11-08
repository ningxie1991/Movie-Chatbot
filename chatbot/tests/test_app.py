from chatbot.speakeasy.app import App


if __name__ == "__main__":
    app = App()
    while True:
        try:
            question = input("Ask:")
            response = app.get_response(question)
        except Exception as e:
            print("Error:", e)

# questions = ['I am a big fan of Steven Spielberg, could you recommend some of his action movies?',
#              'I like the Jurassic Park movie; can you recommend any similar movies?',
#              'Did Christopher Nolan ever work on a Batman movie?',
#              'Who is the director of the Batman movie?',
#              'What is the name of the lead actor in the movie Catch Me If You Can?',
#              # 'Who is the role of Robert Downey Jr. in the Iron Man movie?',
#              'Did Robert Downey Jr. ever appear in an Avengers movie?',
#              # 'Did Robert Downey Jr. ever appear in an Iron Man movie?',
#              # 'Did Christopher Nolan ever work on a Marvel movie?'
#              ]
#
# app = App()
# for q in questions:
#     response = app.get_response(q)

