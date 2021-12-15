from pandas import json_normalize
from qwikidata.sparql import return_sparql_query_results


sparql_query = '''
        SELECT DISTINCT ?targetLabel WHERE
        { 
            
        ?x0 <http://www.wikidata.org/prop/direct/P57> ?target .
            
            values ?x0 { wd:Q810857 wd:Q57394119 wd:Q4869384 wd:Q18914861 wd:Q540890 wd:Q5723590 wd:Q64658410 wd:Q2695156 wd:Q116852 wd:Q1247201 wd:Q596699 wd:Q245863 wd:Q15635431 wd:Q18844637 wd:Q2891561 wd:Q2891582 wd:Q63919331 wd:Q383811 wd:Q673517 wd:Q810858 wd:Q810861 wd:Q4869380 wd:Q512835 wd:Q17996919 wd:Q2401367 wd:Q2690648 wd:Q1990704 wd:Q13415681 wd:Q635933 wd:Q21095079 wd:Q2121056 wd:Q4869347 wd:Q2111133 wd:Q16155099 wd:Q30501762 wd:Q2891476 wd:Q920793 wd:Q14772351 wd:Q112912 wd:Q166262 wd:Q221345 wd:Q2917080 wd:Q2891537 wd:Q3271336 wd:Q2709431 wd:Q10375036 wd:Q498757 wd:Q387696 wd:Q979831 wd:Q1573706 wd:Q61117344 wd:Q29011652 wd:Q4353841 wd:Q2891534 wd:Q16200150 wd:Q2527522 wd:Q14783913 wd:Q20058570 wd:Q25631093 wd:Q22249835 wd:Q176376 wd:Q189054 wd:Q2384094 wd:Q4869383 wd:Q16531880 wd:Q604864 wd:Q3504716 wd:Q3129837 wd:Q13499404 wd:Q276523 wd:Q2287397 wd:Q23013169 wd:Q1339570 wd:Q26684198 wd:Q129161 }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        ORDER BY ASC(?targetLabel)
        LIMIT 10
        '''

query = '''
        SELECT DISTINCT ?targetLabel WHERE
        { 
            { ?x0 ?p ?x1. }
            UNION
            { ?x1 ?p ?x0. }
            values ?x0 { wd:Q25191 }
            values ?x1 { wd:Q810857 wd:Q57394119 wd:Q4869384 wd:Q18914861 wd:Q540890 wd:Q5723590 wd:Q64658410 wd:Q2695156 wd:Q116852 wd:Q1247201 wd:Q596699 wd:Q245863 wd:Q15635431 wd:Q18844637 wd:Q2891561 wd:Q2891582 wd:Q63919331 wd:Q383811 wd:Q673517 wd:Q810858 wd:Q810861 wd:Q4869380 wd:Q512835 wd:Q17996919 wd:Q2401367 wd:Q2690648 wd:Q1990704 wd:Q13415681 wd:Q635933 wd:Q21095079 wd:Q2121056 wd:Q4869347 wd:Q2111133 wd:Q16155099 wd:Q30501762 wd:Q2891476 wd:Q920793 wd:Q14772351 wd:Q112912 wd:Q166262 wd:Q221345 wd:Q2917080 wd:Q2891537 wd:Q3271336 wd:Q2709431 wd:Q10375036 wd:Q498757 wd:Q387696 wd:Q979831 wd:Q1573706 wd:Q61117344 wd:Q29011652 wd:Q4353841 wd:Q2891534 wd:Q16200150 wd:Q2527522 wd:Q14783913 wd:Q20058570 wd:Q25631093 wd:Q22249835 wd:Q176376 wd:Q189054 wd:Q2384094 wd:Q4869383 wd:Q16531880 wd:Q604864 wd:Q3504716 wd:Q3129837 wd:Q13499404 wd:Q276523 wd:Q2287397 wd:Q23013169 wd:Q1339570 wd:Q26684198 wd:Q129161 }
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } 
            ?target wikibase:directClaim ?p .
        }
        ORDER BY ASC(?targetLabel)
    '''

res = return_sparql_query_results(sparql_query)
print(res)
data = res['results']['bindings']
df = json_normalize(data, max_level=1)

print(df)
