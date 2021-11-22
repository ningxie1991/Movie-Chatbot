import re


def format_entity(qid, label):
    return f"{label} (wd:{qid})"


def format_image(qid):
    return f"image:{qid}"


def format_relation(relation):
    if re.match(r"the(.*)of", relation):
        return relation
    elif re.match(r"the(.*)", relation):
        return f"{relation} of"
    elif re.match(r"(.*)of", relation):
        return f"the {relation}"
    elif re.match(r"(.*)by|(.*)for", relation):
        return relation
    elif re.match("genre", relation):
        return f"of the {relation}"
    else:
        return f"the {relation} of"
