from chatbot.algorithm.model.predicate_matcher import PredicateMatcher

predicate_matcher = PredicateMatcher()
top_match = predicate_matcher.top_match("the director")
print(top_match)