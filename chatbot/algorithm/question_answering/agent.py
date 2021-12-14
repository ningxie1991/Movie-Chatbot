import re
from chatbot.algorithm.question_answering.service.crowdsource import CrowdSource
from chatbot.data.dataset import Dataset
from chatbot.algorithm.question_answering.answer.formatter import format_entity, format_relation, format_image
from chatbot.algorithm.question_answering.query.rdf_query_service import RDFQueryService
from chatbot.algorithm.question_answering.question.parser import QuestionParser
from chatbot.algorithm.question_answering.service.image import ImageService
from chatbot.algorithm.question_answering.service.embedding import EmbeddingService


class Agent:
    def __init__(self):
        dataset = Dataset()
        self.question_parser = QuestionParser()
        self.rdf_query_service = RDFQueryService(dataset.graph)
        self.embedding_service = EmbeddingService(dataset.graph)
        self.image_service = ImageService(dataset.graph)
        self.crowd_source = CrowdSource()
        print("Agent initialized")

    def answer(self, question):
        question_type, entities, relation = self.question_parser.parse(question)

        if len(entities) == 0:
            return "Sorry, I didn't understand your question. Could you please spell check and proper case movie titles and person names?"

        response = ''
        if len(entities) > 0:
            if question_type == "wh":
                try:
                    results = self.rdf_query_service.query_wh(entities, relation)
                    if results.empty:
                        response = f"Sorry, I don't know the answer."
                    else:
                        if len(results) == 1 or re.search(r"main|lead|leading|only|best|top", relation):
                            result = results.iloc[0]
                            obj, obj_label = self.embedding_service.validate_answer(result['Subject'], result['Relation'], result['Object'], result['ObjectLabel'])
                            formatted_label = format_entity(obj, obj_label)
                            response = formatted_label
                            crowd_answer = self.crowd_source.find_answer(result['Subject'], result['Relation'], result['Object'])
                            if crowd_answer:
                                response += f" - according to the crowd, who had an inter-rater agreement of {crowd_answer[2]} in this batch; " \
                                            f"the answer distribution for this task was {crowd_answer[0]} support vote(s) and {crowd_answer[1]} reject vote(s). "
                        else:
                            topK = results[:3]
                            relation_wo_article = re.sub(r'^the ', '', relation)
                            # response = f"There are a few {relation_wo_article}s{subject}, for example, "
                            response = f"There are a few results, for example, "
                            for index, row in topK.iterrows():
                                crowd_answer = self.crowd_source.find_answer(row['Subject'], row['Relation'], row['Object'])
                                obj, obj_label = self.embedding_service.validate_answer(row['Subject'],
                                                                                        row['Relation'],
                                                                                        row['Object'],
                                                                                        row['ObjectLabel'])
                                formatted_label = format_entity(obj, obj_label)
                                if topK.shape[0] == 1:
                                    response += f"{formatted_label}."
                                elif index == topK.shape[0] - 1:
                                    response += f"and {formatted_label}."
                                else:
                                    response += f"{formatted_label}, "
                except Exception as e:
                    response = f"Sorry, I don't know the answer."
                    print("Error:", e)
            elif question_type == "yesno":
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
            elif question_type == "recommender" or question_type == "embedding" or question_type == "media":
                try:
                    if question_type == "embedding":
                        results = self.embedding_service.top_match(entities)
                    elif question_type == "media":
                        results = self.image_service.top_match(entities, relation)
                    else:
                        results = self.rdf_query_service.query_action(entities)

                    if results.empty:
                        response = f"Sorry, I can't find it."
                    else:
                        if question_type == "media":
                            result = results.iloc[0]
                            formatted_subject = format_entity(result['Entity'], result['EntityLabel'])
                            formatted_img = format_image(result['Target'])
                            response = f"{formatted_subject} {formatted_img}"
                        else:
                            topK = results[:3]
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
