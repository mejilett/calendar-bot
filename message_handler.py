# registry of previously handled messages
# since the API has no way to tell us we've already done this one
previously_handled_messages = []
BOT_NAME = "final-porject"

def handle_message(message):
  if (message['id'] in previously_handled_messages):
    print("Message id " + message['id'] + " already seen. Skipping.")
    return None
  else:
    # not in so we can process
    # first add to list
    previously_handled_messages.append(message['id'])
