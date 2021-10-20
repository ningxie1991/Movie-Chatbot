import requests, json, time

# url of the speakeasy server
url = "https://speakeasy.ifi.uzh.ch"

r = requests.get(url + "/client-specs")
spec = json.loads(r.text)

# user login
def login(username: str, password: str):
    return requests.post(url=url + "/api/login", json={"username": username, "password": password})

# check details of the current user
def current(session_token: str):
    return requests.get(url=url + "/api/user/current", params={"session": session_token})

# user logout
def logout(session_token: str):
    return requests.get(url=url + "/api/logout", params={"session": session_token})

# check available chat rooms
def check_rooms(session_token: str):
    return requests.get(url=url + "/api/rooms", params={"session": session_token})

# check the state of a chat room
def check_room_state(room_id: str, since: int, session_token: str):
    return requests.get(url=url + "/api/room/{}/{}".format(room_id, since), params={"roomId": room_id, "since": since, "session": session_token})

# post a message to a chat room
def post_message(room_id: str, session_token: str, message: str):
    return requests.post(url=url + "/api/room/{}".format(room_id), params={"roomId": room_id, "session": session_token}, data=message)