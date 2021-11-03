from chatbot.algorithm.data.dataset import Dataset
from chatbot.algorithm.model.entity_matcher import EntityMatcher

dataset = Dataset()
graph = dataset.get_graph()
entity_matcher = EntityMatcher(graph)
entity = 'fictional character'
match_node = entity_matcher.top_match(entity)
print("\n--- the matching node of \"{}\" is {}\n".format(entity, match_node))
