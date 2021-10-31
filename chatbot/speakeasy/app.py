import json
import requests
import time

from chatbot.algorithm.data.dataset import Dataset
from chatbot.algorithm.model.entity_matcher import EntityMatcher
from chatbot.algorithm.model.predicate_matcher import PredicateMatcher
from chatbot.algorithm.model.question_parser import QuestionParser


class App:
    def __init__(self):
        # url of the speakeasy server
        self.url = "https://speakeasy.ifi.uzh.ch"
        # load config from a json file
        with open("../../config/credentials.json", "r") as f:
            credentials = json.load(f)
        self.username = credentials["agent"]["username"]
        self.password = credentials["agent"]["password"]
        self.agent_details = None
        self.graph = Dataset('../../data/14_graph.nt')
        self.question_parser = QuestionParser('../algorithm/saved_models/Movies_NER.sav')
        self.entity_matcher = EntityMatcher(self.graph)
        self.predicate_matcher = PredicateMatcher('../../data/wikidata/graph_properties_expanded.csv')

    # user login
    def login(self):
        self.agent_details = requests.post(url=self.url + "/api/login",
                                           json={"username": self.username, "password": self.password}).json()
        print("--- agent details:")
        print(json.dumps(self.agent_details, indent=4))

    # check details of the current user
    def current(self, session_token: str):
        return requests.get(url=self.url + "/api/user/current", params={"session": session_token})

    # user logout
    def logout(self, session_token: str):
        return requests.get(url=self.url + "/api/logout", params={"session": session_token})

    # check available chat rooms
    def check_rooms(self, session_token: str):
        return requests.get(url=self.url + "/api/rooms", params={"session": session_token})

    # check the state of a chat room
    def check_room_state(self, room_id: str, since: int, session_token: str):
        return requests.get(url=self.url + "/api/room/{}/{}".format(room_id, since),
                            params={"roomId": room_id, "since": since, "session": session_token})

    # post a message to a chat room
    def post_message(self, room_id: str, session_token: str, message: str):
        return requests.post(url=self.url + "/api/room/{}".format(room_id),
                             params={"roomId": room_id, "session": session_token}, data=message)

    def start_chat(self):
        chatroom_messages = {}
        while True:
            current_rooms = self.check_rooms(session_token=self.agent_details["sessionToken"]).json()["rooms"]
            print("--- {} chatrooms available".format(len(current_rooms)))

            for idx, room in enumerate(current_rooms):
                room_id = room["uid"]
                print("chat room - {}: {}".format(idx, room_id))

                new_room_state = self.check_room_state(room_id=room_id, since=0,
                                                       session_token=self.agent_details["sessionToken"]).json()
                new_messages = new_room_state["messages"]
                print("found {} messages".format(len(new_messages)))

                if room_id not in chatroom_messages.keys():
                    chatroom_messages[room_id] = []

                if len(chatroom_messages[room_id]) != len(new_messages):
                    for message in new_messages:
                        if message["ordinal"] >= len(chatroom_messages[room_id]) and message["session"] != \
                                self.agent_details["sessionId"]:
                            # process the message and find answer
                            response = self.find_answer(message["message"])
                            self.post_message(room_id=room_id, session_token=self.agent_details["sessionToken"],
                                              message=response)

                chatroom_messages[room_id] = new_messages

            time.sleep(3)
            print("")

    def find_answer(self, question):
        response = "Hello , I got your message \"{}\" at {}.".format(question, time.strftime("%H:%M:%S, %d-%m-%Y",
                                                                                             time.localtime()))

        ### Part 1: Fact-oriented questions ###
        # 1. get the movie-domain entities in the question
        entities = self.question_parser.get_entities(question)

        # 2. get the non-entity nouns in the question
        nouns = self.question_parser.get_nouns()

        # 3. get the verbs in the question
        verbs = self.question_parser.get_verbs()

        # 4. find question pattern using nouns and verbs and determine the relation
        # 5. match the relation with predicate
        # 6. match the entity with a node in the graph
        # 7. perform SPARQL query to find the answer
        # 8. formulate the answer as a response

        return response
