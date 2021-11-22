import re

from chatbot.data.dataset import Dataset
from chatbot.algorithm.question_answering.answer.formatter import format_entity, format_relation, format_image
from chatbot.algorithm.question_answering.query.rdf_query_service import RDFQueryService
from chatbot.algorithm.question_answering.question.parser import QuestionParser
from chatbot.algorithm.question_answering.question.patterns import is_wh_question, get_relation, \
    main_actor_character_pattern, is_yesno_question, is_action_question, is_recommender_question, \
    is_image_question
from chatbot.algorithm.question_answering.service.image import ImageService
from chatbot.algorithm.question_answering.service.recommender import RecommenderService


class Agent:
    def __init__(self):
        dataset = Dataset()
        self.question_parser = QuestionParser()
        self.rdf_query_service = RDFQueryService(dataset.graph)
        self.recommender_service = RecommenderService(dataset.graph)
        self.image_service = ImageService(dataset.graph)
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

            if is_wh_question(question, first_entity[0]):
                try:
                    relation = get_relation(question, first_entity[0])
                    results = self.rdf_query_service.query_wh(entities, relation)
                    if results.empty:
                        response = f"Sorry, I don't know the answer."
                    else:
                        if len(results) == 1 or re.search(main_actor_character_pattern, relation):
                            result = results.iloc[0]
                            formatted_label = format_entity(result['Target'], result['TargetLabel'])
                            # response = f"{relation.capitalize()}{subject} is {formatted_label}."
                            response = formatted_label
                        else:
                            topK = results[:3]
                            relation_wo_article = re.sub(r'^the ', '', relation)
                            # response = f"There are a few {relation_wo_article}s{subject}, for example, "
                            response = f"There are a few results, for example, "
                            for index, row in topK.iterrows():
                                formatted_label = format_entity(row['Target'], row['TargetLabel'])
                                if topK.shape[0] == 1:
                                    response += f"{formatted_label}."
                                elif index == topK.shape[0] - 1:
                                    response += f"and {formatted_label}."
                                else:
                                    response += f"{formatted_label}, "
                except Exception as e:
                    response = f"Sorry, I don't know the answer."
                    print("Error:", e)
            elif is_yesno_question(question):
                try:
                    results = self.rdf_query_service.query_yesno(entities)
                    if results.empty:
                        response = f"No, I don't think so."
                    else:
                        topK = results[:3]
                        formatted_subject = format_entity(topK['Subject'].iloc[0], topK['SubjectLabel'].iloc[0])
                        response = f"Yes, {formatted_subject} is "
                        for index, row in topK.iterrows():
                            formatted_object = format_entity(row['Object'], row['ObjectLabel'])
                            formatted_relation = format_relation(row['RelationLabel'])
                            if topK.shape[0] == 1:
                                response += f"{formatted_relation} {formatted_object}."
                            elif index == topK.shape[0] - 1:
                                response += f"and {formatted_relation} {formatted_object}."
                            else:
                                response += f"{formatted_relation} {formatted_object}, "
                except Exception as e:
                    response = f"Sorry, I don't know the answer."
                    print("Error:", e)
            elif is_action_question(question):
                try:
                    relation = get_relation(question, first_entity[0])
                    if is_recommender_question(relation) or is_image_question(relation):
                        results = self.non_query_answer(entities, relation)
                    else:
                        results = self.rdf_query_service.query_action(entities)

                    if results.empty:
                        response = f"Sorry, I can't."
                    else:
                        if is_image_question(relation):
                            result = results.iloc[0]
                            formatted_subject = format_entity(result['Entity'], result['EntityLabel'])
                            formatted_img = format_image(result['Target'])
                            response = f"{formatted_subject} {formatted_img}"
                        else:
                            topK = results[:3]
                            relation_wo_article = re.sub(r'^the ', '', relation)
                            response = f"How about these:  "
                            for index, row in topK.iterrows():
                                formatted_label = format_entity(row['Target'], row['TargetLabel'])
                                if topK.shape[0] == 1:
                                    response += f"{formatted_label}."
                                elif index == topK.shape[0] - 1:
                                    response += f"and {formatted_label}."
                                else:
                                    response += f"{formatted_label}, "
                except Exception as e:
                    response = f"Sorry, I don't know the answer."
                    print("Error:", e)

            else:
                response = f"Sorry, I don't know the answer."
        return response

    def non_query_answer(self, entities, relation):
        if is_recommender_question(relation):
            return self.recommender_service.top_match(entities, relation)
        elif is_image_question(relation):
            return self.image_service.top_match(entities, relation)
        else:
            return None
