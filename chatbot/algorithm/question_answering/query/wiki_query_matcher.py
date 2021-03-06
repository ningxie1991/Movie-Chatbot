import re

entity_type_map = {'TITLE': 'wd:Q11424 wd:Q24856 wd:Q5398426',
                   'CHARACTER': 'wd:Q95074 wd:Q15773347 wd:Q15632617 wdt:P1441 wdt:P674',
                   'ACTOR': 'wd:Q33999 wdt:P161 wdt:P175',
                   'DIRECTOR': 'wdt:P57',
                   'GENRE': 'wdt:P136'
                   }


def wh_query(entities, relation, predicate):
    variables = '?target ?targetLabel'
    where_clause = ''
    filter_clause = ''
    union_clause = ''
    for index, entity in enumerate(entities):
        if entity[1] == 'CHARACTER' and re.search("actor", relation):
            pred = 'http://www.wikidata.org/prop/direct/P175'
        else:
            pred = predicate[0]
        original_label = entity[0]
        original_label_clean = re.sub('[,;.\?]', '', entity[0])
        variables += f''' ?x{index} ?x{index}Label '''
        union_clause += f'''
              {{ ?x0 rdfs:label "{original_label}"@en . }}
              UNION
              {{ ?x0 skos:altLabel "{original_label}"@en . }}
              UNION
              {{ ?x0 rdfs:label "{original_label_clean}"@en . }}
              UNION
              {{ ?x0 skos:altLabel "{original_label_clean}"@en . }}'''

        where_clause += f'''
              ?x{index} wdt:P31 ?type .
              VALUES ?type {{ {entity_type_map[entity[1]]} }}
              OPTIONAL {{ ?x{index} wdt:P577 ?date . }}
              ?x{index} <{pred}> ?target .
              OPTIONAL {{
                  ?y wdt:P179 ?x{index}.
                  OPTIONAL {{ ?y wdt:P577 ?date . }}
                  ?y <{pred}> ?target.  
              }}'''

        if entity[2] and len(entity[2]) > 0:
            candidates = " ".join(f"wd:{c}" for c in entity[2])
            filter_clause += f'''VALUES ?x{index} {{ {candidates} }}'''

    query = f'''
        SELECT DISTINCT {variables} WHERE
        {{ 
            {union_clause}
            UNION
            {{ {filter_clause} }}
            {where_clause}
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        ORDER BY DESC(year(?date))
        LIMIT 30
    '''
    print(f"---------- query: \n{query}")
    return query


def yesno_query(entities):
    variables = '?targetLabel'
    where_clause = ''
    with_clause = ''
    include_clause = ''
    for index, entity in enumerate(entities):
        variables += f''' ?x{index} ?x{index}Label '''
        original_label = entity[0]
        original_label_clean = re.sub('[,;.\?]', '', entity[0])

        union_clause = f'''
            {{ ?x{index} rdfs:label "{original_label}"@en . }}
            UNION
            {{ ?x{index} skos:altLabel "{original_label}"@en . }}
            UNION
            {{ ?x{index} rdfs:label "{original_label_clean}"@en . }}
            UNION
            {{ ?x{index} skos:altLabel "{original_label_clean}"@en . }}
        '''

        if entity[2] and len(entity[2]) > 0:
            candidates = " ".join(f"wd:{c}" for c in entity[2])
            union_clause += f'''
            UNION
            {{ values ?x{index} {{ {candidates} }} }}'''

        with_clause += f'''
        WITH 
        {{
            select ?x{index} ?x{index}Label 
            where {{
                {union_clause}
            }}
        }} AS %x{index}'''

        include_clause += f'''
                INCLUDE %x{index}'''

        if index < len(entities) - 1:
            if index == 0:
                where_clause += f'''
                {{ ?x{index} ?p ?x{index + 1}. }}
                UNION
                {{ ?x{index + 1} ?p ?x{index}. }}'''
            else:
                where_clause += f'''
                UNION
                {{ ?x{index} ?p ?x{index + 1}. }}
                UNION
                {{ ?x{index + 1} ?p ?x{index}. }}'''

    query = f'''
        SELECT DISTINCT {variables}
        {with_clause}
        WHERE
        {{ 
            {include_clause}
            {where_clause}
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
            ?target wikibase:directClaim ?p .
        }}
        ORDER BY ASC(?targetLabel)
        LIMIT 30
    '''
    print(f"---------- query: \n{query}")
    return query


def action_query(entities, relation):
    where_clause = ''
    for index, entity in enumerate(entities):
        entity_type = entity[1]
        if entity_type == 'TITLE':
            where_clause += f'''
                          ?target ?p{index} ?x{index}.
                          VALUES ?x{index} {{ {entity_type_map[entity[1]]} }}'''

            if entity[2] and len(entity[2]) > 0:
                candidates = " ".join(f"wd:{c}" for c in entity[2])
                where_clause += f'''VALUES ?target {{ {candidates} }}'''
        else:
            where_clause += f'''
              ?target ?p{index} ?x{index}.
              VALUES ?p{index} {{ {entity_type_map[entity[1]]} }}'''

            if entity[2] and len(entity[2]) > 0:
                candidates = " ".join(f"wd:{c}" for c in entity[2])
                where_clause += f'''
                VALUES ?x{index} {{ {candidates} }}'''

            if entity_type == 'GENRE' and re.search('movie|film', relation):
                where_clause += f'''
                ?target wdt:P31 ?type
                VALUES ?type {{ {entity_type_map['TITLE']} }}'''

    query = f'''
            SELECT DISTINCT ?target ?targetLabel
            WHERE
            {{ 
                {where_clause}
                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
            }}
            LIMIT 30
        '''
    print(f"---------- query: \n{query}")
    return query
