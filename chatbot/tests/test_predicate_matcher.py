from chatbot.algorithm.predicate_linker import PredicateLinker

predicate_matcher = PredicateLinker()
top_match = predicate_matcher.top_match("star in")
print(top_match)