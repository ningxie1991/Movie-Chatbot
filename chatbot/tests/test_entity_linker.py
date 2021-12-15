from chatbot.algorithm.entity_linker import EntityLinker

entity_matcher = EntityLinker()
entity = 'batman'
candidates = entity_matcher.get_candidates(entity)
print(f"\n--- the candidates of \"{entity}\" are {candidates}\n")


