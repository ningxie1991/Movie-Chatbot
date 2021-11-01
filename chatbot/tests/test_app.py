# query_template = '''
#         PREFIX ddis: <http://ddis.ch/atai/>
#         PREFIX wd: <http://www.wikidata.org/entity/>
#         PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#         PREFIX schema: <http://schema.org/>
#
#         SELECT ?movie ?lbl WHERE {
#             ?movie wdt:P31 wd:Q5398426 ;
#                    rdfs:label "{}"@en ;
#                    <{}> ?x .
#             ?x rdfs:label ?y
#         }
#         '''.format(entity, match_pred)

# query_template = '''
#         PREFIX ddis: <http://ddis.ch/atai/>
#         PREFIX wd: <http://www.wikidata.org/entity/>
#         PREFIX wdt: <http://www.wikidata.org/prop/direct/>
#         PREFIX schema: <http://schema.org/>
#
#         SELECT ?movie ?lbl WHERE {
#             <{}> <{}> ?x .
#             ?x rdfs:label ?y
#         }
#         '''.format(match_entity, match_pred)