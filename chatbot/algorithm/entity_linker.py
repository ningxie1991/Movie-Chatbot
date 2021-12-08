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
        if self.genres['EntityLabel'].str.contains(entity_string, regex=False).any():
            return "GENRE"
        elif self.movies['EntityLabel'].str.contains(entity_string, regex=False).any():
            return "TITLE"
        elif self.characters['EntityLabel'].str.contains(entity_string, regex=False).any():
            return "CHARACTER"
        elif self.directors['EntityLabel'].str.contains(entity_string, regex=False).any():
            return "DIRECTOR"
        elif self.actors['EntityLabel'].str.contains(entity_string, regex=False).any():
            return "ACTOR"
        else:
            return original_label

    def get_candidates(self, entity_string, label):
        if label == "GENRE":
            return self.genres.loc[self.genres['EntityLabel'].str.contains(entity_string, regex=False), 'Entity'].drop_duplicates().tolist()
        elif label == "TITLE":
            return self.movies.loc[self.movies['EntityLabel'].str.contains(entity_string, regex=False), 'Entity'].drop_duplicates().tolist()
        elif label == "CHARACTER":
            return self.characters.loc[self.characters['EntityLabel'].str.contains(entity_string, regex=False), 'Entity'].drop_duplicates().tolist()
        elif label == "DIRECTOR":
            return self.directors.loc[self.directors['EntityLabel'].str.contains(entity_string, regex=False), 'Entity'].drop_duplicates().tolist()
        elif label == "ACTOR":
            return self.actors.loc[self.actors['EntityLabel'].str.contains(entity_string, regex=False), 'Entity'].drop_duplicates().tolist()
        else:
            return self.graph_entities.loc[self.graph_entities['EntityLabel'].str.contains(entity_string, regex=False), 'Entity'].drop_duplicates().tolist()
