from chatbot.question_answering.question.parser import QuestionParser


question_parser = QuestionParser()

# print("\n------- Sentence: {}".format('Who is the actor of the character Thor?'))
# entities, bos = question_parser.parse('Who is the actor of the character Thor?')
# query = question_parser.query_wh('Who is the actor of the character Thor?', entities)
# # Who is the actor of the character Iron Man?

# print("\n------- Sentence: {}".format('Did Christopher Nolan ever work on a Batman movie?'))
# entities, bos = question_parser.parse('Did Christopher Nolan ever work on a Batman movie?')
# query = question_parser.query_yesno(entities)

# 'I like the Jurassic Park movie; can you recommend any similar movies?'
# 'I am a big fan of Steven Spielberg, could you recommend some of his action movies?'
print("\n------- Sentence: {}".format('I am a big fan of Steven Spielberg, could you recommend some of his action movies?'))
entities, bos = question_parser.parse('I am a big fan of Steven Spielberg, could you recommend some of his action movies?')
query = question_parser.query_action('I am a big fan of Steven Spielberg, could you recommend some of his action movies?', entities)
# Who is the actor of the character Iron Man?

