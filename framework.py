import requests
import time
#import message_handler

BOT_TOKEN = ""
PROJECT_ROOM_ID = "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vNDE2MTM2ODAtY2E4MC0xMWYwLTgyNjAtNTVhZTBhYzkxNzYw"

# simple authorized_get
def authorized_get(endpoint, params=None):
  r = requests.get("https://webexapis.com/v1" + endpoint,
                   headers = {"Authorization": "Bearer " + BOT_TOKEN},
                   params = params)
  return r

def authorized_post(endpoint, params=None, data=None):
  r = requests.post("https://webexapis.com/v1" + endpoint,
                    headers = {"Authorization": "Bearer " + BOT_TOKEN, "Content-Type": "application/json"},
                    params = params,
                    post_data = data)

# this returns the bot id and information
# not terribly useful but good for debug on startup
def get_self():
  r = authorized_get("/people/me")
  if (r.status_code == 401):
    print("You probably forgot to add the key!")
    print("Exiting.")
    raise SystemExit
  return r.json()

# grabs the rooms the bot is in
# for now just grab the first and use it
# should only be in 1 anyway
def get_rooms():
  api_fetch = authorized_get("/rooms")
  return api_fetch.json()['items']

# fetches a specific room by ID
# this is so i can hardcode the room
def get_room_by_id(rooms, id):
  for room in rooms:
    if (room['id'] == id):
      return room
  return None

# gets the message
# because of webex api, i can only get messages that mention the bot
def get_message(room_id, count=1):
  api_fetch = authorized_get("/messages", params = {"roomId": room_id, "max": count, "mentionedPeople": "me"})
  return api_fetch.json()

# sends a message
# assuming i did it right
def post_message(room_id, text):
  api_response = authorized_posts("/messages", data = {"roomId": room_id, "text": text})
  return api_response.json()

# this function starts up the bot and inits the main loop
def main():
  print("Hello World!")
  bot_data = get_self()
  self_id = bot_data['id']
  bot_name = bot_data['displayName']
  print(f"Started bot {bot_name}.")

  rooms = get_rooms()
  room = get_room_by_id(rooms, PROJECT_ROOM_ID)
  print(f"Found {len(rooms)} rooms. Arbitrarilty selecting room {room['title']}")
  print(f"Room ID: {room['id']}")

  # main loop
  # basically grabs messages and passes them to message handlers
  while True:
    poll_interval = 2000
    time.sleep(poll_interval/1000) # 2 ms poll interval
    message = get_message(room['id'])
    
  

main()
