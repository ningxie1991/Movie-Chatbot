import re
from chatbot.question_answering.answer.formatter import format_link, format_relation
from chatbot.question_answering.question.parser import QuestionParser
from chatbot.question_answering.question.patterns import main_actor_character_pattern, get_relation, \
    is_wh_question, is_yesno_question, is_action_question, is_non_query
from chatbot.question_answering.sparql_query.query_service import sparql_request


class Agent:
    def __init__(self):
        self.question_parser = QuestionParser()
        self.verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.wh_pos = ['WDT', 'WP', 'WP$', 'WRB']

    def answer(self, question):
        entities = self.question_parser.parse(question)

        if len(entities) == 0:
            return "Sorry, I didn't understand your question. Could you please spell check and capitalize the first letters of movie titles and names?"

        response = ''
        if len(entities) > 0:
            first_entity = entities[0]
            entity_label = re.sub('[,;\?]', '', first_entity[0])
            subject = f" of {entity_label}"

            if is_wh_question(question):
                relation = get_relation(question)
                query = self.question_parser.query_wh(entities, relation)
                if not query:
                    response = f"Sorry, I don't know how to look up the answer for this question."
                else:
                    results = sparql_request(query)
                    if results and len(results) > 0:
                        if len(results) == 1 or re.search(main_actor_character_pattern, relation):
                            result = results[0]
                            formatted_label = format_link(result[0], result[1])
                            response = f"{relation.capitalize()}{subject} is {formatted_label}."
                        else:
                            topK = results[:3]
                            relation_wo_article = re.sub(r'^the ', '', relation)
                            response = f"There are more than one {relation_wo_article}s{subject}. Some results are: "
                            for index, result in enumerate(topK):
                                formatted_label = format_link(result[0], result[1])
                                if index == len(topK) - 1:
                                    response += f"{formatted_label}."
                                else:
                                    response += f"{formatted_label}, "
                    else:
                        response = f"Sorry, I can't find out {relation}{subject}. Better luck next time!"
            elif is_yesno_question(question):
                query = self.question_parser.query_yesno(entities)
                if not query:
                    response = f"Sorry, I don't know how to look up the answer for this question."
                else:
                    results = sparql_request(query)
                    if results and len(results) > 0:
                        topK = results[:3]
                        first = results[0]
                        formatted_label = format_link(first[1], first[2])
                        response = f"Yes, {formatted_label} is "
                        for index, result in enumerate(topK):
                            formatted_label = format_link(result[3], result[4])
                            formatted_relation = format_relation(result[0])
                            if len(topK) == 1:
                                response += f"{formatted_relation} {formatted_label}."
                            elif index == len(topK) - 1:
                                response += f"and {formatted_relation} {formatted_label}."
                            else:
                                response += f"{formatted_relation} {formatted_label}, "
                    else:
                        response = f"No, I don't think so."
            elif is_action_question(question):
                relation = get_relation(question)
                if is_non_query(relation):
                    print("should use recommendation system and image system")
                else:
                    query = self.question_parser.query_action(entities, relation)
                    if not query:
                        response = f"Sorry, I don't know how to look up the answer for this question."
                    else:
                        results = sparql_request(query)
                        if results and len(results) > 0:
                            topK = results[:3]
                            relation_wo_article = re.sub(r'^the ', '', relation)
                            response = f"Here are some {relation_wo_article}{subject} I recommend: "
                            for index, result in enumerate(topK):
                                formatted_label = format_link(result[0], result[1])
                                if index == len(topK) - 1:
                                    response += f"{formatted_label}."
                                else:
                                    response += f"{formatted_label}, "
                        else:
                            response = f"Sorry, I can't."
            else:
                response = f"Sorry, I don't know."
        return response
