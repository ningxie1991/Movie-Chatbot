from chatbot.data.dataset import Dataset
from chatbot.my_entity_linker.entity_linker import EntityLinker

dataset = Dataset()
graph = dataset.get_graph()
entity_matcher = EntityLinker(graph)
entity = 'character'
match_node = entity_matcher.top_match(entity)
print(f"\n--- the matching node of \"{entity}\" is {match_node}\n")
