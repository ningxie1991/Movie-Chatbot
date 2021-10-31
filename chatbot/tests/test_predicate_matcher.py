from chatbot.algorithm.model.predicate_matcher import PredicateMatcher

predicate_matcher = PredicateMatcher('../../data/wikidata/graph_properties_expanded.csv')
top_match = predicate_matcher.top_match("the lead actor")
print(top_match)