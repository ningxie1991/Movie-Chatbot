from chatbot.question_answering.question.parser import QuestionParser


question_parser = QuestionParser()

print("\n------- Sentence: {}".format('Who is the actor of the character Thor?'))
entities, bos = question_parser.parse('Who is the actor of the character Thor?')
query = question_parser.query_wh('Who is the actor of the character Thor?', entities)
# Who is the actor of the character Iron Man?

# print("\n------- Sentence: {}".format('Did Christopher Nolan ever work on a Batman movie?'))
# entities, bos = question_parser.parse('Did Christopher Nolan ever work on a Batman movie?')
# query = question_parser.query_yesno(entities)



