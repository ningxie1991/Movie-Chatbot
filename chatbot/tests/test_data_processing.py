import os
import re

import numpy as np
import pandas as pd

# dataset = Dataset()
# graph = dataset.get_graph()
# process_graph(graph)

dirname = os.path.dirname(__file__)
entities = pd.read_csv(os.path.join(dirname, '../../data/ddis/14_graph_entities.csv'))
name = 'MTV Movie Award for Best Scared-As-S**t Performance'
re_name = re.escape('MTV Movie Award for Best Scared-As-S**t Performance')
print(re_name)
contains = entities[entities['Name'].str.contains(re_name)]

same_name_qids = contains.loc[contains['Name'] == name, 'QID'].values
similar_name_qids = contains.loc[contains['Name'] != name, 'QID'].values
same_name_count = same_name_qids.shape[0]
similar_name_count = np.shape(similar_name_qids)[0]
base_prob = 0.6/(same_name_count + similar_name_count)
same_name_probs = [(base_prob + 0.4/same_name_count) for qid in same_name_qids]
similar_name_probs = [base_prob for qid in similar_name_qids]
qids = np.append(same_name_qids, similar_name_qids)
probs = same_name_probs + similar_name_probs
print(qids)
print(probs)
