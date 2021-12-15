import os
import pandas as pd


class EntityLinker:
    def __init__(self):
        # load the entities
        dirname = os.path.dirname(__file__)
        self.graph_entities = pd.read_csv(os.path.join(dirname, '../../data/ddis/graph_entities.csv'))
        self.movies = pd.read_csv(os.path.join(dirname, '../../data/ddis/entity_categories/movie_entities.csv'))
        self.directors = pd.read_csv(os.path.join(dirname, '../../data/ddis/entity_categories/director_entities.csv'))
        self.actors = pd.read_csv(os.path.join(dirname, '../../data/ddis/entity_categories/actor_entities.csv'))
        self.characters = pd.read_csv(os.path.join(dirname, '../../data/ddis/entity_categories/character_entities.csv'))
        self.genres = pd.read_csv(os.path.join(dirname, '../../data/ddis/entity_categories/genre_entities.csv'))
        print("EntityLinker initialized")

    def disambiguation(self, entity_string, original_label):
        if self.genres['EntityLabel'].str.lower().str.contains(entity_string.lower(), regex=False).any():
            return "GENRE"
        elif self.movies['EntityLabel'].str.lower().str.contains(entity_string.lower(), regex=False).any():
            return "TITLE"
        elif self.characters['EntityLabel'].str.lower().str.contains(entity_string.lower(), regex=False).any():
            return "CHARACTER"
        elif self.actors['EntityLabel'].str.lower().str.contains(entity_string.lower(), regex=False).any():
            return "ACTOR" if original_label != "DIRECTOR" else original_label
        elif self.directors['EntityLabel'].str.lower().str.contains(entity_string.lower(), regex=False).any():
            return "DIRECTOR" if original_label != "ACTOR" else original_label
        else:
            return original_label

    def get_candidates(self, entity_string):
        primary_candidates = self.graph_entities.loc[self.graph_entities['EntityLabel'].str.lower() == entity_string.lower(), 'Entity'].drop_duplicates().tolist()
        secondary_candidates = self.graph_entities.loc[self.graph_entities['EntityLabel'].str.lower().str.contains(entity_string.lower(), regex=False), 'Entity'].drop_duplicates().tolist()
        return primary_candidates, secondary_candidates



