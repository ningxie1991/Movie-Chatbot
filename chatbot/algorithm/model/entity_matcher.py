import editdistance


class EntityMatcher:
    def __init__(self, graph):
        self.graph = graph

    def top_match(self, entity, query):
        nodes = {}
        for row in self.graph.query(query):
            nodes[row['key'].toPython()] = row['lbl'].toPython()

        tmp = 9999
        match_node = ""
        for key, value in nodes.items():
            if editdistance.eval(value, entity) < tmp:
                tmp = editdistance.eval(value, entity)
                match_node = key
        return match_node
