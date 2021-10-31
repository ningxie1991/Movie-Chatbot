import pandas as pd
from chatbot.algorithm.dataset import Dataset
from chatbot.algorithm.util.data_util import read_data, elaborate_property_labels


def process_mit_movies_data():
    train = read_data('../../data/mit_movies_corpus/engtrain.bio')
    train.to_csv("../../data/mit_movies_corpus/engtrain_cased.csv", index=False)

    test = read_data('../../data/mit_movies_corpus/engtest.bio')
    test.to_csv("../../data/mit_movies_corpus/engtest_cased.csv", index=False)


def map_wikidata_properties():
    dataset = Dataset('../../data/14_graph.nt')
    graph = dataset.get_graph()
    print("Parsed graph")

    # get all the distinct wikidata properties from the graph
    graph_properties = graph.query('''
        PREFIX ns1: <http://www.wikidata.org/prop/direct/>

        SELECT DISTINCT ?p WHERE {
            ?s ?p ?o
            FILTER( STRSTARTS(str(?p), str(ns1:)) )
        }
        '''
                                   )

    # pre-saved all the properties and their labels from wikidata
    wikidata_properties = pd.read_csv('../../data/wikidata/properties.csv')
    df = elaborate_property_labels(graph_properties, wikidata_properties)
    df.to_csv("../../data/wikidata/graph_properties_expanded.csv", index=False)
