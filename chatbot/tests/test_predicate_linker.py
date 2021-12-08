from chatbot.algorithm.predicate_linker import PredicateLinker

predicate_matcher = PredicateLinker()
top_match = predicate_matcher.top_match("director")
print(top_match)
