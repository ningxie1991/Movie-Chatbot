import queue
import threading

from chatbot.speakeasy.app import App

if __name__ == "__main__":
    app = App()
    while True:
        question = input("Ask:")
        threads = []
        q = queue.Queue()
        try:
            t = threading.Thread(target=app.get_response, args=(question, q,))
            t.start()
            t.join()
            response = q.get()
            print(f"A: {response}\n")
        except Exception as e:
            print("Error:", e)

# questions = [
#              "Who is the director of the Batman movie?",
#              "Who's the director of the Batman movie?",
#              'Did Christopher Nolan ever work on a Batman movie?',
#              'What is the name of the lead actor in the movie Catch Me If You Can?',
#              'I like the Jurassic Park movie; can you recommend any similar movies?',
#              'I am a big fan of Steven Spielberg, could you recommend some of his action movies?',
#              'Show me the pictures of the lead actors of the movie Jurassic Park.',
#              'Can you show me the poster of the movie Batman?',
#              'Show me an action movie poster.',
#              "What's the box office of the movie E.T. the Extra-Terrestrial?"
#              ]
#
# app = App()
# for question in questions:
#     threads = []
#     q = queue.Queue()
#     try:
#         t = threading.Thread(target=app.get_response, args=(question, q,))
#         t.start()
#         t.join()
#         response = q.get()
#         print(f"A: {response}\n")
#     except Exception as e:
#         print("Error:", e)

