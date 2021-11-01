from chatbot.algorithm.data.dataset import Dataset
from chatbot.algorithm.model.entity_matcher import EntityMatcher

movie_query = '''
        PREFIX ddis: <http://ddis.ch/atai/> 
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        PREFIX schema: <http://schema.org/> 

        SELECT ?key ?lbl WHERE {
            ?key wdt:P31 wd:Q11424 ;
                   rdfs:label ?lbl 
        }
        '''

dataset = Dataset('../../data/14_graph.nt')
graph = dataset.get_graph()
entity_matcher = EntityMatcher(graph, movie_query)
entity = 'Batman'
match_node = entity_matcher.top_match(entity)
print("\n--- the matching node of \"{}\" is {}\n".format(entity, match_node))
