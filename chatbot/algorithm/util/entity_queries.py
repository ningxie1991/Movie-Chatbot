movie_query = '''
        PREFIX ddis: <http://ddis.ch/atai/> 
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        PREFIX schema: <http://schema.org/> 

        SELECT ?movie ?lbl WHERE {
            ?movie wdt:P31 wd:Q11424 ;
                   rdfs:label ?lbl 
        }
        '''

tv_series_query = '''
        PREFIX ddis: <http://ddis.ch/atai/> 
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        PREFIX schema: <http://schema.org/> 

        SELECT ?movie ?lbl WHERE {
            ?movie wdt:P31 wd:Q5398426 ;
                   rdfs:label ?lbl 
        }
        '''