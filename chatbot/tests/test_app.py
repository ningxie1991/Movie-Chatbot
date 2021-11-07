from chatbot.speakeasy.app import App


# if __name__ == "__main__":
#     app = App()
#     while True:
#         try:
#             question = input("Ask:")
#             response = app.get_response(question)
#         except Exception as e:
#             print("Error:", e)

questions = ['Did Christopher Nolan ever work on a Batman movie?',
             'Who is the director of the Batman movie?',
             'What is the name of the lead actor in the movie Catch Me If You Can?',
             'Who is the actor of the Iron Man character?',
             'Did Robert Downey Jr. ever appear in an Avengers movie?',
             'Did Robert Downey Jr. ever appear in an Iron Man movie?',
             'Did Christopher Nolan ever work on a Marvel movie?']

app = App()
for q in questions:
    response = app.get_response(q)

