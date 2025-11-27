#from webexteamssdk import WebexTeamsAPI
import requests
#import jsonify

#api = WebexTeamsAPI(access_token=key)
#id = api.people.me().id

#app = Flask(__name__)

def send_message_to_room(room_id: str, text: str):
#  api.messages.create(roomId=room_id, markdown=text)
  pass

def handle_help_command(room_id: str):
  help_text = "Hello!"
  send_message_to_room(room_id, help_text)

def handle_unknown(room_id: str):
  send_message_to_room(room_id, "Unknown command.")

def handle_message(text: str, room_id: str):
  normalized = text.strip().lower()
  if normalized in ("/help", "help"):
    handle_help_command(room_id)
  else:
    handle_unknown()

#@app.route('/webhook', methods=['POST'])
def webhook():
  webhook_data = request.json
  handle_webhook(webhook_data)
  return jsonify({"success": True})

def authorized_get(endpoint):
  r = requests.get("https://webexapis.com/v1" + endpoint,
                   headers = {"Authorization": "Bearer " + key})
  return r

def get_self():
  r = authorized_get("/people/me")
  return r.json()

def get_rooms():
  api_fetch = authorized_get("/rooms")
  return api_fetch.json()['items']

self_id = get_self()
#print(get_self())

rooms = get_rooms()
room = rooms[0]
print(f"Found {len(rooms)} rooms. Selecting room {room['title']}")

# main loop
while True:
  
