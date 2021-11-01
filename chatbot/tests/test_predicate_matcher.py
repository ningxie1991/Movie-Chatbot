import os

from chatbot.algorithm.model.predicate_matcher import PredicateMatcher

dirname = os.path.dirname(__file__)
embeds_dir = os.path.join(dirname, '../../data/wikidata/property_embeds.npy')
properties_dir = '../../data/wikidata/graph_properties_expanded.csv'
predicate_matcher = PredicateMatcher(properties_dir, embeds_dir)

top_match = predicate_matcher.top_match("the director")
print(top_match)