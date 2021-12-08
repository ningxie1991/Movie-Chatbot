import re

wh_pattern = r"(?:Who |What |Which |Where |When |who |what |which |where |when |" \
             r"Who's |What's |Which's |Where's |When's |who's |what's |which's |where's |when's |" \
             r"Who're |What're |Which're |Where're |When're |who're |what're |which're |where're |when're )" \
             r"(?:is |are |was |were )?(.*)(?: in| of| from| for)(?: the| a)?(?: movie| film |character)?"


def wh_pattern_B(entity):
    return f"(?:Who |What |Which |Where |When |who |what |which |where |when |" \
           f"Who's |What's |Which's |Where's |When's |who's |what's |which's |where's |when's |" \
           f"Who're |What're |Which're |Where're |When're |who're |what're |which're |where're |when're )" \
           f"(?:movie |movies |film |films )?(?:is |are |was |were |did )?{entity} (.*)"


about_pattern = r"(?:What |what |What's |what's |What're | what're )(?:is |are |was |were )?(.*)about"

yesno_pattern = "(Is|Was|Are|Were|Does|Do|Did|is|was|are|were|does|do|did) "

action_pattern_A = r".*?(?:Show|show|Find|find|Recommend|recommend)(?: me)?(?: some| any| a few)? (.*)(?: of)"
action_pattern_B = r".*?(?:Show|show|Find|find|Recommend|recommend)(?: me)?(?: some| any| a few)?(?: of)?(?: his| hers| theirs)? (.*)"

main_actor_character_pattern = 'main actor|lead actor|main character|lead character'

image_pattern_A = r"poster|posters|picture|pictures|image|images|photo|photos|scene|frame"
image_pattern_B = r"(?:What |How |what |how |What's |How's |what's |how's )(?:do |does |is |are )?(.*)(?: look like| like)"

recommender_pattern = r"similar"


def is_wh_question(question, label):
    return re.match(wh_pattern, question) or re.match(wh_pattern_B(label), question)


def is_yesno_question(question):
    return re.match(yesno_pattern, question)


def is_action_question(question):
    return re.match(action_pattern_A, question) or re.match(action_pattern_B, question) or re.match(image_pattern_B, question)


def is_recommender_question(target_type):
    return re.search(recommender_pattern, target_type)


def is_image_question(target_type, question):
    return re.search(image_pattern_A, target_type) or re.match(image_pattern_B, question)


def get_relation(question, label):
    relation = ''
    if re.match(wh_pattern, question):
        relation = re.match(wh_pattern, question).groups()[0]
    elif re.match(wh_pattern_B(label), question):
        relation = re.match(wh_pattern_B(label), question).groups()[0]
    elif re.match(action_pattern_A, question):
        relation = re.match(action_pattern_A, question).groups()[0]
    elif re.match(action_pattern_B, question):
        relation = re.match(action_pattern_B, question).groups()[0]
    return re.sub('[,;\?]', '', relation) if relation else ''
