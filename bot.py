import os
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI
from calendar_ops import get_upcoming_events, format_events_for_message

# ----------------------------
# FLASK APP INIT
# ----------------------------

app = Flask(__name__)

# ----------------------------
# WEBEX CONFIG
# ----------------------------

WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN")

if not WEBEX_BOT_TOKEN:
    raise RuntimeError("WEBEX_BOT_TOKEN not set as an environment variable.")

api = WebexTeamsAPI(access_token=WEBEX_BOT_TOKEN)


def get_bot_person_id():
    """Get the bot's own Webex personId so we can ignore our own messages."""
    me = api.people.me()
    return me.id


BOT_PERSON_ID = get_bot_person_id()

# ----------------------------
# MESSAGE SENDING
# ----------------------------

def send_message_to_room(room_id: str, text: str):
    """Send a markdown message to a Webex room."""
    api.messages.create(roomId=room_id, markdown=text)

# ----------------------------
# BOT COMMANDS
# ----------------------------

def handle_help_command(room_id: str):
    help_text = (
        "👋 **Hi! I'm your Calendar Reminder Bot.**\n\n"
        "Available commands:\n"
        "- `/reminders` — show upcoming deadlines from Google Calendar\n"
        "- `/help` — show this help message\n"
    )
    send_message_to_room(room_id, help_text)


def handle_reminders_command(room_id: str):
    try:
        events = get_upcoming_events(max_events=5)
        if not events:
            send_message_to_room(room_id, "✅ No upcoming events found.")
            return

        message = format_events_for_message(events)
        send_message_to_room(room_id, message)

    except Exception as e:
        print(f"[ERROR] Failed to fetch reminders: {e}")
        send_message_to_room(
            room_id,
            "⚠️ I ran into an issue fetching calendar reminders. Please try again later."
        )


def handle_message(text: str, room_id: str):
    """Route incoming text to the right command handler."""
    normalized = text.strip().lower()

    if normalized in ("/help", "help"):
        handle_help_command(room_id)
    elif normalized in ("/reminders", "reminders", "deadlines"):
        handle_reminders_command(room_id)
    else:
        send_message_to_room(
            room_id,
            "🤖 Unknown command.\n"
            "Try `/reminders` or `/help`."
        )

# ----------------------------
# WEBHOOK ENDPOINT
# ----------------------------

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Webex will POST here when a message is created.
    Your webhook in Webex must point to this URL.
    """
    data = request.json
    print(f"[DEBUG] Webhook payload: {data}")

    if not data or "data" not in data:
        return "No data", 400

    message_id = data["data"]["id"]
    room_id = data["data"]["roomId"]
    person_id = data["data"]["personId"]

    # Ignore messages from the bot itself
    if person_id == BOT_PERSON_ID:
        return "Ignored self", 200

    # Fetch full message and handle it
    message = api.messages.get(message_id)
    text = message.text or ""

    handle_message(text, room_id)
    return "OK", 200

# ----------------------------
# MAIN ENTRYPOINT
# ----------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"✅ Bot starting on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
