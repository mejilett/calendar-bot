import os
import calendar-ops.py
from flask import Flask, request
from webexteamssdk import WebexTeamsAPI

WEBEX_TOKEN = 'YOUR_TOKEN_HERE'
api = WebexTeamsAPI(access_token=WEBEX_TOKEN)

def schedule_messsage(message):
    room_id = message.roomId
    message_text = message.text.strip()

    if message_text.startswith('/create'): 
        words = message_text.split()
        api.messages.create(
            roomId=room_id, 
            text="/create [title] [date] [title]"
        )
        return
    title = ''.join(words[1:-2])
    date = words[-2]
    time = words[-1]
    result = calendar-ops.create_event(title, date, time)

    api.messages.create(
        roomID=room_id,
        text=f"Meeting created!"
    )

    if message_text.startswith('/delete'):
        term = message_text.split()
        api.messages.create(
            roomId=room_id,
            text="/delete [event_id]"
            )
        return
