from pandas import json_normalize
from qwikidata.sparql import return_sparql_query_results


def sparql_request(query):
    try:
        res = return_sparql_query_results(query)
        data = res['results']['bindings']
        df = json_normalize(data, max_level=1)
        if df.empty:
            return None
        else:
            results = list(df.filter(like='value').to_records(index=False))
            return results
    except Exception as e:
        print("Error:", e)
        return None


# def format_query_results(results):
