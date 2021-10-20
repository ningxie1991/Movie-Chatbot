from utils import *

#load credentials from a json file
with open("./credentials.json", "r") as f:
    credentials = json.load(f)
username = credentials["agent"]["username"]
password = credentials["agent"]["password"]

agent_details = login(username=username, password=password).json()
print("--- agent details:")
print(json.dumps(agent_details, indent=4))

chatroom_messages = {}
while True:
    current_rooms = check_rooms(session_token=agent_details["sessionToken"]).json()["rooms"]
    print("--- {} chatrooms available".format(len(current_rooms)))

    for idx, room in enumerate(current_rooms):
        room_id = room["uid"]
        print("chat room - {}: {}".format(idx, room_id))

        new_room_state = check_room_state(room_id=room_id, since=0, session_token=agent_details["sessionToken"]).json()
        new_messages = new_room_state["messages"]
        print("found {} messages".format(len(new_messages)))

        if room_id not in chatroom_messages.keys():
            chatroom_messages[room_id] = []

        if len(chatroom_messages[room_id]) != len(new_messages):
            for message in new_messages:
                if message["ordinal"] >= len(chatroom_messages[room_id]) and message["session"] != agent_details["sessionId"]:
                    response = "Hello , I got your message \"{}\" at {}.".format(message["message"], time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime()))
                    post_message(room_id=room_id, session_token=agent_details["sessionToken"], message=response)

        chatroom_messages[room_id] = new_messages

    time.sleep(3)
    print("")



