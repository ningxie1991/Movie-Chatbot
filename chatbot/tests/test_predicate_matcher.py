from chatbot.my_predicate_linker.predicate_linker import PredicateLinker

predicate_matcher = PredicateLinker()
top_match = predicate_matcher.top_match("the lead actor")
print(top_match)