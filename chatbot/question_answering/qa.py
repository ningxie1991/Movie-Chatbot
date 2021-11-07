import re

from pandas import json_normalize
from qwikidata.sparql import return_sparql_query_results

from chatbot.question_answering.question.parser import QuestionParser
from chatbot.question_answering.question.patterns import yesno_pattern, wh_pattern, main_actor_character_pattern


class Agent:
    def __init__(self):
        self.question_parser = QuestionParser()
        self.verb_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.wh_pos = ['WDT', 'WP', 'WP$', 'WRB']

    def answer(self, question):
        entities, bos = self.question_parser.parse(question)

        if len(entities) == 0:
            return "Sorry, I didn't understand your question. Could you please spell check and capitalize the first letters of movie titles and names?"

        response = ''
        bos_word = bos[0]
        bos_pos = bos[1]
        if len(entities) > 0:
            first_entity = entities[0]
            if bos_pos in self.wh_pos and re.match(wh_pattern.format(first_entity[0]), question):
                query, relation = self.question_parser.query_wh(question, entities)

                if not query:
                    response = f"Sorry, I don't know how to look up the answer for this question."
                else:
                    res = return_sparql_query_results(query)
                    data = res['results']['bindings']
                    df = json_normalize(data, max_level=1)

                    subject = ''
                    for entity, tag, candidates in entities:
                        entity_label = re.sub('[,;.\?]', '', entity)
                        subject += f" of {entity_label}"

                    if df.empty:
                        response = f"Sorry, I can't find out {relation}{subject}. Better luck next time!"
                    else:
                        results = list(df.filter(like='value').to_records(index=False))
                        if len(results) > 0:
                            if len(results) == 1 or re.search(main_actor_character_pattern, relation):
                                result = results[0]
                                response = f"{relation.capitalize()}{subject} is <a href='{result[0]}' title='{result[1]}' target='_blank'>{result[1]}</a>."
                            else:
                                topK = results[:3]
                                relation_wo_article = re.sub(r'^the ', '', relation)
                                response = f"There are more than one {relation_wo_article}s{subject}. Some results are: "
                                for index, result in enumerate(topK):
                                    if index == len(topK) - 1:
                                        response += f"<a href='{result[0]}' title='{result[1]}' target='_blank'>{result[1]}</a>."
                                    else:
                                        response += f"<a href='{result[0]}' title='{result[1]}' target='_blank'>{result[1]}</a>, "
                        else:
                            response = f"Sorry, I can't find out {relation}{subject}. Better luck next time!"

            elif bos_pos in self.verb_pos and re.match(yesno_pattern, bos_word.lower()):
                query = self.question_parser.query_yesno(entities)
                if not query:
                    response = f"Sorry, I don't know how to look up the answer for this question."
                else:
                    res = return_sparql_query_results(query)
                    data = res['results']['bindings']
                    df = json_normalize(data, max_level=1)

                    if df.empty:
                        response = f"No, I don't think so."
                    else:
                        results = list(df.filter(like='value').to_records(index=False))
                        if len(results) == 1:
                            result = results[0]
                            if re.match(r"a|e|i|o|u", result[0]):
                                article = 'an'
                            else:
                                article = 'a'
                            response += f"<a href='{result[1]}' title='{result[2]}' target='_blank'>{result[2]}</a> is {article} {result[0]} of <a href='{result[3]}' title='{result[4]}' target='_blank'>{result[4]}</a>."
                        elif len(results) > 1:
                            topK = results[:3]
                            first = results[0]
                            response = f"Yes, <a href='{first[1]}' title='{first[2]}'>{first[2]}</a> is "
                            for index, result in enumerate(topK):
                                if index == len(topK) - 1:
                                    response += f"and the {result[0]} of <a href='{result[3]}' title='{result[4]}' target='_blank'>{result[4]}</a>."
                                else:
                                    response += f"the {result[0]} of <a href='{result[3]}' title='{result[4]}' target='_blank'>{result[4]}</a>, "

                        else:
                            response = f"No, I don't think so."
            else:
                response = f"Sorry, I don't know."
        return response
