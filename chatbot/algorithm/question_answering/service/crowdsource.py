import os
import pandas as pd
import re
from rdflib import Namespace, URIRef, Literal, XSD


class CrowdSource:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.crowd_data = pd.read_csv(os.path.join(dirname, '../../../../data/ddis/filtered_crowd_data_ISO_dates.csv'))
        print("CrowdSource initialized")

    def merge_data(self, graph):
        WD = Namespace('http://www.wikidata.org/entity/')
        WDT = Namespace('http://www.wikidata.org/prop/direct/')
        DDIS = Namespace('http://ddis.ch/atai/')
        grouped = self.crowd_data.groupby('HITId')
        for hitId, group in grouped:
            hit = group.iloc[0]
            votes = group['AnswerLabel'].value_counts().to_frame('count').reset_index()
            # majority_vote = votes['index'].iloc[0]
            # if majority_vote == 'CORRECT':
            # merge crowd data with graph
            s = URIRef(WD[re.sub("wd:", "", hit['Input1ID'])])

            p_value = hit['Input2ID']
            if re.search("ddis:", p_value):
                p = URIRef(DDIS[re.sub("ddis:", "", p_value)])
            else:
                p = URIRef(WDT[re.sub("wdt:", "", p_value)])

            o_value = hit['Input3ID']
            if re.search("wd:", o_value):
                o = URIRef(WD[re.sub("wd:", "", o_value)])
            elif re.search(r'(\d+-\d+-\d+)', o_value):
                o = Literal(o_value, datatype=XSD.date)
            else:
                o = Literal(o_value)
            if not (s, p, o) in graph:
                graph.add((s, p, o))

    def find_answer(self, s, p, o):
        df = self.crowd_data
        crowd_answers = df.loc[(df['Input1ID'] == s) & (df["Input2ID"] == p) & (df["Input3ID"] == o)]
        if crowd_answers.empty:
            return None
        else:
            kappa = crowd_answers['Kappa'].iloc[0]
            votes = crowd_answers['AnswerLabel'].value_counts().to_frame('count').reset_index()
            if votes.loc[votes['index'] == 'CORRECT', 'count'].values:
                support_votes = votes.loc[votes['index'] == 'CORRECT', 'count'].values[0]
            else:
                support_votes = 0

            if votes.loc[votes['index'] == 'INCORRECT', 'count'].values:
                reject_votes = votes.loc[votes['index'] == 'INCORRECT', 'count'].values[0]
            else:
                reject_votes = 0
            return support_votes, reject_votes, round(kappa, 2)