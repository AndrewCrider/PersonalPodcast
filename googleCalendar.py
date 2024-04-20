from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import timedelta, datetime
from dateutil import parser
import google.generativeai as genai
import json
import configparser
import pytz

with open('supportFiles/supportFiles.json', 'r') as json_file:
    config_data = json.load(json_file)

calendarsToSync = config_data["calendarsToSync"]
config = configparser.ConfigParser()
config.read('config.ini')
gemini_api_key = config['gemini']['apiKey']
credentials_file = config['googleJsonFileLocation']['jsonFile']

class googleCalendar:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.service = None

    def authenticate(self):
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=['https://www.googleapis.com/auth/calendar'])

        self.service = build('calendar', 'v3', credentials=creds)

    def get_events(self, calendar_id, start_date, end_date):
        start = start_date.isoformat() + 'Z'
        end = end_date.isoformat() + 'Z'

        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        
        return events

def formatDateForTimeZone(googleUTCDate):
    
    if googleUTCDate.get('dateTime') is not None:
        dt = parser.parse(googleUTCDate['dateTime'])
        
        # Check if the datetime string contains a timezone offset
        if dt.utcoffset() is not None:
            dt = dt.astimezone(pytz.utc)
            
    elif 'date' in googleUTCDate:
        dt = parser.parse(googleUTCDate['date'])
    else:
        return datetime.datetime.now()

    # Convert to UTC timezone
    dt_utc = dt.replace(tzinfo=pytz.UTC)

    # Convert to America/New_York timezone
    #TODO: Change to your timezone here
    ny_timezone = pytz.timezone('America/New_York')
    dt_ny = dt_utc.astimezone(ny_timezone)

    # Format the datetime string without timezone offset
    formatted_datetime = dt_ny.strftime('%A, %Y-%m-%d %H:%M:%S')
    
    return formatted_datetime

def getTodaysEvents():
    
    google_calendar = googleCalendar(credentials_file)
    google_calendar.authenticate()

    start_date = datetime.now()
    
    # TODO: You Can Modify the days value to bring in more events
    end_date = start_date + timedelta(days=2)
    event_list = []
    events_toRead_out = []

    for c in calendarsToSync:
       
        events = google_calendar.get_events(c['calendarid'], start_date, end_date)

        for event in events:
            
            event_dict = {
                "id": event["id"],
                "calendar_id": c['calenderFriendly'],
                "summary": event["summary"],
                "location": event.get('location', None),
                "description": event.get('description', None),
                "htmlLink": event["htmlLink"],
                "colorId": event.get('colorId', None),
                "start": formatDateForTimeZone(event["start"]),
                "end": formatDateForTimeZone(event["end"])
            }
            event_list.append(event_dict)
        
        #TODO: Add Day Name
    for el in event_list:
        event_text = f"At {el['start']} you have {el['summary']} that ends at {el['end']} for calendar {el['calendar_id']}"
        events_toRead_out.append(event_text)
    
    return events_toRead_out


def geminiSummary():
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    #TODO: Add Day Name
    prompt_prefix = "You are a scheduling assistant I will give you a list of calendar events. Turn it into a list of events  " + \
                    "Be upbeat and excited about the events.  Try to group it by calendar, but choose chronology over that factor"+ \
                    f"Do not return any special characters and format it as a paragraph.  Today's date is {datetime.now()} and I'm in the America/New_York timezone" + \
                    "BEGIN Calendar Events LIST:\n"

    todaysEvents = getTodaysEvents()
    
    
    if len(todaysEvents) > 0:
        CalendarSummaryRequest = prompt_prefix + str(todaysEvents)
        
        response = model.generate_content(CalendarSummaryRequest)
        returnText = response.text
    else:
        returnText = "You're all clear today!  Enjoy your day"

    return returnText

