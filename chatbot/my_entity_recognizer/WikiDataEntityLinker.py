import pandas as pd


class WikiDataEntityLinker:
    def __init__(self, graph):
        self.graph = graph

    def get_candidates(self, label):
        query = '''
           PREFIX ddis: <http://ddis.ch/atai/>
           PREFIX wd: <http://www.wikidata.org/entity/>
           PREFIX wdt: <http://www.wikidata.org/prop/direct/>
           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

           SELECT ?entity ?typeLabel WHERE
           {{
                ?entity rdfs:label "{}"@en;
                        wdt:P31 ?type .
                ?type rdfs:label ?typeLabel
           }}
           LIMIT 100
       '''.format(label)
        candidates = []
        for row in self.graph.query(query):
            candidates.append((row['entity'], row['typeLabel']))
        return pd.DataFrame(candidates, columns=['Entity', 'Type'])


