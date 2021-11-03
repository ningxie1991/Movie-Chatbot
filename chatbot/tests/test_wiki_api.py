from pandas import json_normalize
from qwikidata.sparql import return_sparql_query_results


sparql_query = '''
        SELECT ?characterLabel ?actorLabel
        WHERE
        {{
          ?film rdfs:label "{}"@en .
          ?film p:P161 [
                ps:P161 ?actor;
                pq:P453 ?character
          ].
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        LIMIT 10
    '''.format("Catch Me If You Can")

query = '''
        SELECT ?targetLabel WHERE
        { 
            {
                ?entity rdfs:label "Batman"@en .
                ?entity wdt:P57 ?target .
            }
            UNION
            {
                ?entity rdfs:label "Batman"@en .
                ?target wdt:P57 ?entity .
            }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        ORDER BY ASC(?targetLabel) 
        LIMIT 10
    '''

res = return_sparql_query_results(query)
print(res)

# Json looks like this:
# { 'head': {
#       'vars': ['characterLabel', 'actorLabel']
#    },
#   'results': {
#       'bindings': [
#           {'characterLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Frank Abagnale'},
#             'actorLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Leonardo DiCaprio'}
#            }
#       ]
#   }
# }

# How to make it look like this?
# characterLabel   actorLabel
# Frank Abagnale   Leonardo DiCaprio


# data = res['results']['bindings']
# df = json_normalize(data, max_level=1)
#
# df1 = df[['characterLabel.value', 'actorLabel.value']]
# print(df1)
