import re


class QuestionPattern:
    def __init__(self):
        # wh-questions
        self.wh = r"(?:Who |What |Which |Where |When |who |what |which |where |when |" \
                     r"Who's |What's |Which's |Where's |When's |who's |what's |which's |where's |when's |" \
                     r"Who're |What're |Which're |Where're |When're |who're |what're |which're |where're |when're )" \

        self.wh_ner_A = self.wh + r"(?:is |are |was |were |does |do |did )?(.*)(?: in| of| from| for)(?: the| a)?(?: movie| film |character)?"
        self.wh_ner_B_2 = self.wh + r"(?:movie |movies |film |films )?(?:is |are |was |were |does |do |did )?(.*) (.*)"

        self.wh_A = self.wh + r"(?:is |are |was |were )?(.*)(?: in| of| from| for)(?: the| a)?(.*)(?: movie| film |character)([\w\s]*)"
        self.wh_B = self.wh + r"(?:is |are |was |were )?(.*)(?: in| of| from| for)(?: the| a)?(.*)"
        self.wh_C = self.wh + r"(?:movie |movies |film |films )?(?:is |are |was |were |did )?(.*)(?:by)(.*)"
        self.wh_D = self.wh + r"(?:movie |movies |film |films )?(?:is |are |was |were |did )?(.*) (.*)"

        self.wh_type = r"(?:What |what |What's |what's )(?:is |are |was |were )?" \
                          r"(?:a |an |the |the type of |the parent type of |the parent of |the class of |the parent class of )?(.*)"

        # yes/no-questions
        self.yesno_pattern = "(Is|Was|Are|Were|Does|Do|Did|is|was|are|were|does|do|did) "

        # recommender-questions #TODO - combine all action questions to recommender questions
        recommender = r"I(?: like| love| am a big fan of| am a fan of)(?: the)?(.*)(?: movie| movies| film| films| series)?(?:, |. |; )"
        self.recommender_A = recommender + r"(?:could you |can you |Could you |Can you )(?:show |find |recommend |suggest )(?:me)?(.*)(?: of| by| directed by| featuring| starring)(?: his| hers| theirs| the movie| the film| the series| the)?(.*)"
        self.recommender_B = recommender + r"(?:could you |can you |Could you |Can you )(?:show |find |recommend |suggest )(?:me)?(.*)(?: movies| movie| films| film)(.*)"
        self.recommender_C = recommender + r"(?:could you |can you |Could you |Can you )(?:show |find |recommend |suggest )(?:me)?(.*)"
        self.recommender_D = r".*?(?:Show|show|Find|find|Recommend|recommend|Suggest|suggest)(?: me)?(.*)(?: of| by| directed by| featuring| starring)(?: his| hers| theirs| the movie| the film| the series| the)?(.*)"
        self.recommender_E = r".*?(?:Show|show|Find|find|Recommend|recommend|Suggest|suggest)(?: me)?(.*)(?: movies| movie| films| film)(.*)"
        self.recommender_F = r".*?(?:Show|show|Find|find|Recommend|recommend|Suggest|suggest)(?: me)?(.*)"

        self.recommender_ner_A = r"(?:.*)(?:Show|show|Find|find|Recommend|recommend|Suggest|suggest)(?: me)?(?: some| any| a few)? (.*)(?: of| by| directed by| featuring| starring)(?: his| hers| theirs| the movie| the film| the series| the)?(.*)"
        self.recommender_ner_B = r"(?:.*)(?:Show|show|Find|find|Recommend|recommend|Suggest|suggest)(?: me)?(.*)"

        self.main_actor_character_pattern = 'main actor|lead actor|main character|lead character'

        self.image_pattern_A = r"poster|posters|picture|pictures|image|images|photo|photos|scene|frame"
        self.image_pattern_B = r"(?:What |How |what |how |What's |How's |what's |how's )(?:do |does |is |are )?(.*)(?: look like| like)"

        self.embedding_pattern = r"similar"
        print("QuestionPattern initialized")

    def wh_ner_B(self, entity):
        return self.wh + f"(?:movie |movies |film |films )?(?:is |are |was |were |does |do |did )?{entity} (.*)" if entity else self.wh_ner_B_2

    def categorize_question_type(self, question, is_ner=True, entity=None):
        if self.is_wh_question(question, is_ner, entity):
            return "wh", self.is_wh_question(question, is_ner, entity).groups()
        elif self.is_yesno_question(question):
            return "yesno", []
        elif self.is_recommender_question(question, is_ner):
            return "recommender", self.is_recommender_question(question, is_ner).groups()
        else:
            return "unknown", []

    def is_wh_question(self, question, is_ner=True, entity=None):
        if is_ner:
            return re.match(self.wh_ner_A, question) or re.match(self.wh_ner_B(entity), question) or re.match(self.wh_type, question)
        else:
            return re.match(self.wh_A, question) or re.match(self.wh_B, question) \
                   or re.match(self.wh_C, question) or re.match(self.wh_type, question)

    def is_yesno_question(self, question):
        return re.match(self.yesno_pattern, question)

    def is_recommender_question(self, question, is_ner=True):
        if is_ner:
            return re.match(self.recommender_ner_A, question) or re.match(self.recommender_ner_B, question)
        return re.match(self.recommender_A, question) or re.match(self.recommender_B, question) or re.match(self.recommender_C, question) \
            or re.match(self.recommender_D, question) or re.match(self.recommender_E, question) or re.match(self.recommender_F, question)

    def is_embedding_questions(self, question):
        return re.search(self.embedding_pattern, question)

    def is_multi_media_question(self, question):
        return re.search(self.image_pattern_A, question) or re.match(self.image_pattern_B, question)
