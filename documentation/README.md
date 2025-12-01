# Group 4: Allen Liu, Scarlet Mejia
# Calendar Bot Documentation

The following is a brief documentation of the functionality of the calendar bot.

### Clear explanation of what your workflow does
Calendar Bot works through a Cisco Webex bot with integration with Google Calendar. The bot includes several commands, including the ability to schedule meetings and notify of meetings coming soon.

### List of technologies used and how they connect
The bot uses three core technologies:
1. Cisco Webex Rooms
2. Cisco Webex Apps
3. Google Calendar
4. Docker

Cisco Webex Rooms are used to send and receive messages to the bot. The bot sends and receives messages from the Cisco Webex Room, then processes and sends events to Google Calendar to be created.

Docker can be used to automatically startup and shutdown the bot in a containerized Ubuntu image.

### Setup instructions
The bot can be set up by entering the bot token and the room ID into the `framework.py` file. From there, you can run `framework.py` using Python 3.

### Any code/ config files
For now, there are no config files, though you can manually create and read config files yourself.
