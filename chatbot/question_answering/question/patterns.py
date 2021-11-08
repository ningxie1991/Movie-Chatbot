
# Examples of wh_pattern:
#
# Who is [the director] of the [Batman] movie?
# What is [the name of the lead actor] in the movie [Catch Me If You Can]?
# Which is [the main character] of the [Avengers] movie?
# Where is [the film location] of the [Iron Man] movie?
# Who is the actor for Tony Stark?
# Which character did Robert Downy Jr play in the Avengers movie?
import re

wh_pattern = r"(?:Who |What |Which |Where )(?:is |are |was |were )(.*)(?: in| of| from| for)(?: the| a)?(?: movie| film |character)?"

about_pattern = r"What (?:is |are |was |were )(.*)about"

yesno_pattern = "(Is|Was|Are|Were|Does|Do|Did|is|was|are|were|does|do|did) "

action_pattern_A = r".*?(?:Show|show|Find|find|Recommend|recommend)(?: me)?(?: some| any| a few)?(?: of)?(?: his| hers| theirs)? (.*)"
action_pattern_B = r".*?(?:Show|show|Find|find|Recommend|recommend)(?: me)?(?: some| any| a few)? (.*)(?: of)"

main_actor_character_pattern = 'main actor|lead actor|main character|lead character'

non_query_pattern = r"poster|posters|picture|pictures|image|images|similar"


def is_wh_question(question):
    return re.match(wh_pattern, question) or re.match(about_pattern, question)


def is_yesno_question(question):
    return re.match(yesno_pattern, question)


def is_action_question(question):
    return re.match(action_pattern_A, question) or re.match(action_pattern_B, question)


def is_non_query(target_type):
    return re.search(non_query_pattern, target_type)


def get_relation(question):
    relation = ''
    if re.match(wh_pattern, question):
        relation = re.match(wh_pattern, question).groups()[0]
    elif re.match(about_pattern, question):
        relation = "main subject"
    elif re.match(action_pattern_A, question):
        relation = re.match(action_pattern_A, question).groups()[0]
    elif re.match(action_pattern_B, question):
        relation = re.match(action_pattern_B, question).groups()[0]
    return re.sub('[,;\?]', '', relation) if relation else ''
