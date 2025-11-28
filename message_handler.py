BOT_NAME = "final-porject"

# registry of previously handled messages
# since the API has no way to tell us we've already done this one
previously_handled_messages = []

# core message handler
# first checks if message has been seen before
# then removes the prefix and parses the command
# then passes to a handler
def handle_message(message):
  # if we seen before, print id and quantity, then skip
  if (message['id'] in previously_handled_messages):
    print(f"Message id {id_trunc(message['id'])} already seen. {len(previously_handled_messages)} messages seen so far. Skipping.")
    return None
  else:
    # not in so we can process
    # first add to list
    previously_handled_messages.append(message['id'])
    print(f"New message {id_trunc(message['id'])}: {message['text']}")
    
    # use BOT_NAME as prefix
    message_text = message['text']
    message_text = message_text.strip()
    if (message_text.startswith(BOT_NAME)):
      # trim out BOT_NAME and any leading spaces
      message_text = message_text[len(BOT_NAME):].strip()
      # now we can grab the actual command
      command = parse_command(message_text)
      print(f"Caught command '{message_text}'")

      if (command in ("help", "/help")):
        return help_handler(message_text)
      elif (command in ("hello")):
        return "Hello world!"





      else:
        return None

    return None

# simple help handler
# this should probably be changed!!!!
def help_handler(message_text):
  return "This is my super cool help message!"



# parse a command by basically just grabbing the first word
def parse_command(message_text):
  return message_text.split(' ')[0]

# ids are obnoxiously long, so we just take the first 8 and last 8 chars
def id_trunc(id):
  text = str(id)
  return text[0:8] + "..." + text[96:104]
