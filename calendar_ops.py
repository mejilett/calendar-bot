import datetime
from datetime import timedelta, datetime
import os.path
import pytz

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

def get_calendar_service():
    SCOPES = ["https://www.googleapis.com/auth/calendar"] #full calendar access w/ google calendar api
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=credentials)


def create_event(title, date_str, start_str, duration_min=60):
    service = get_calendar_service()
    timezone = pytz.timezone('America/Los_Angeles')
    start_time_str = f"{date_str} {start_str}"
    start_time = timezone.localize(datetime.strptime(start_time_str, "%Y-%m-%d %H:%M"))
    end_time = start_time + timedelta(minutes=duration_min) #sets end time for meetings
    event = {
        'summary': title, 
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Los_Angeles',    
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },     
    }
    calendar_id = '' #put your own primary google calendar ID 
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print("Event ID: {}".format(event.get('id')))
    print("Event Link: {}".format(event.get('htmlLink')))
    return {"id": event['id'], "link": event.get('htmlLink'), 'title': title, 'date': date_str, 'time': start_str, 'duration': duration_min}

#delete a scheduled meeting
def delete_event(event_id):
    service = get_calendar_service()
    service.events().delete(calendarID='primary', eventId=event_id).execute()
    return {'success': True, 'message': 'Event deleted successfully'}
