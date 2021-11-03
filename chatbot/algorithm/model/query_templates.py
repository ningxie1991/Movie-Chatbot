import re

import pandas as pd


class QuestionTemplates:
    def __init__(self):
        director_for_movie_query = '''?movie ns1:P57 ?director .
                ?director rdfs:label ?lbl .'''

        actor_for_movie_query = '''?movie ns1:P161 ?actor .
                ?actor rdfs:label ?lbl'''

        character_for_movie_query = '''?character ns1:P1441 ?movie .
                ?character rdfs:label ?lbl .'''

        movies_for_director_query = '''?movie ns1:P57 ?director .
                ?movie rdfs:label ?lbl .'''

        movies_for_actor_query = '''?movie ns1:P161 ?actor .
                ?movie rdfs:label ?lbl .'''

        character_for_actor_query = '''?character ns1:P175 ?actor .
                ?character rdfs:label ?lbl .'''

        movies_for_character_query = '''?character ns1:P1441 ?movie .
                ?movie rdfs:label ?lbl .'''

        actor_for_character_query = '''?character ns1:P175 ?actor .
                ?actor rdfs:label ?lbl'''

        self.title_query_df = pd.DataFrame(
            [('director', director_for_movie_query), ('actor', actor_for_movie_query),
             ('character', character_for_movie_query)],
            columns=['relation', 'query'])
        self.director_query_df = pd.DataFrame([('movies', movies_for_director_query)], columns=['relation', 'query'])
        self.actor_query_df = pd.DataFrame(
            [('movies', movies_for_actor_query), ('character', character_for_actor_query)],
            columns=['relation', 'query'])
        self.character_query_df = pd.DataFrame(
            [('movies', movies_for_character_query), ('actor', actor_for_character_query)],
            columns=['relation', 'query'])

    def title_related_query(self, entity, relation):
        query = '''
               PREFIX ddis: <http://ddis.ch/atai/>
               PREFIX wd: <http://www.wikidata.org/entity/>
               PREFIX ns1: <http://www.wikidata.org/prop/direct/>
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

               SELECT ?lbl WHERE {{
                   ?movie rdfs:label "{}"@en .
                   {}
               }}
               LIMIT 10
           '''.format(entity, self.title_query_df.loc[self.title_query_df['relation'] == relation, 'query'].values[0])
        return query

    def director_related_query(self, entity, relation):
        query = '''
            PREFIX ddis: <http://ddis.ch/atai/>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX ns1: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lbl WHERE {{
                ?director rdfs:label "{}"@en .
                {}
            }}
            LIMIT 10
        '''.format(entity,
                   self.director_query_df.loc[self.director_query_df['relation'] == relation, 'query'].values[0])
        return query

    def actor_related_query(self, entity, relation):
        query = '''
            PREFIX ddis: <http://ddis.ch/atai/>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX ns1: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lbl WHERE {{
                ?actor rdfs:label "{}"@en .
                {}
            }}
            LIMIT 10
        '''.format(entity,
                   self.actor_query_df.loc[self.actor_query_df['relation'] == relation, 'query'].values[0])
        return query

    def character_related_query(self, entity, relation):
        query = '''
            PREFIX ddis: <http://ddis.ch/atai/>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX ns1: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lbl WHERE {{
                ?character rdfs:label "{}"@en .
                {}
            }}
            LIMIT 10
        '''.format(entity,
                   self.character_query_df.loc[self.character_query_df['relation'] == relation, 'query'].values[0])
        return query

    @staticmethod
    def find_movie_character_for_actor_query(movie, actor):
        query = '''
            PREFIX ddis: <http://ddis.ch/atai/>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX ns1: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lbl WHERE {{
                ?movie rdfs:label "{}"@en .
                ?character ns1:P1441 ?movie .
                ?character ns1:P175 ?actor .
                ?actor rdfs:label "{}"@en .
                ?character rdfs:label ?lbl .
            }}
            LIMIT 10
        '''.format(movie, actor)
        return query

    @staticmethod
    def find_actor_for_movie_character_query(movie, character):
        query = '''
                PREFIX ddis: <http://ddis.ch/atai/>
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX ns1: <http://www.wikidata.org/prop/direct/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?lbl WHERE {{
                    ?movie rdfs:label "{}"@en .
                    ?character ns1:P1441 ?movie .
                    ?character rdfs:label "{}"@en .
                    ?character ns1:P175 ?actor .
                    ?actor rdfs:label ?lbl .
                }}
                LIMIT 10
            '''.format(movie, character)
        return query

    @staticmethod
    def generate_query(entity, predicate):
        predicate = re.sub("http://www.wikidata.org/prop/direct/", 'ns1:', predicate)
        query = '''
            PREFIX ddis: <http://ddis.ch/atai/>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX ns1: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?lbl WHERE
            {{ 
                {{
                    ?x rdfs:label "{}"@en .
                    ?x {} ?y .
                }}
                UNION
                {{
                    ?x rdfs:label "{}"@en .
                    ?y {} ?x .
                }}
                ?y rdfs:label ?lbl .
            }}
            ORDER BY ASC(?lbl) 
            LIMIT 10
        '''.format(entity, predicate, entity, predicate)
        return query

    @staticmethod
    def generate_wiki_query(entity, predicate):
        predicate = re.sub("http://www.wikidata.org/prop/direct/", 'wdt:', predicate)
        query = '''
                SELECT ?targetLabel WHERE
                {{ 
                    {{
                        ?entity rdfs:label "{}"@en .
                        ?entity {} ?target .
                    }}
                    UNION
                    {{
                        ?entity rdfs:label "{}"@en .
                        ?target {} ?entity .
                    }}
                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
                }} 
                LIMIT 10
            '''.format(entity, predicate, entity, predicate)
        return query

    @staticmethod
    def main_actor_character_query(entity):
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
            '''.format(entity)
        return sparql_query


# ?x ns1:P1441|ns1:P175 ?entity .
# ?x ns1:P31 ?y .
# ?y ns1:P279 wd:Q95074
# ?x rdfs:label ?lbl .