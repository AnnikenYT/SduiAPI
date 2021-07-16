#   _____     _       _  ___  ______ _____   _    _
#  /  ___|   | |     (_)/ _ \ | ___ \_   _| | |  | |
#  \ `--.  __| |_   _ _/ /_\ \| |_/ / | |   | |  | |_ __ __ _ _ __  _ __   ___ _ __
#   `--. \/ _` | | | | |  _  ||  __/  | |   | |/\| | '__/ _` | '_ \| '_ \ / _ \ '__|
#  /\__/ / (_| | |_| | | | | || |    _| |_  \  /\  / | | (_| | |_) | |_) |  __/ |
#  \____/ \__,_|\__,_|_\_| |_/\_|    \___/   \/  \/|_|  \__,_| .__/| .__/ \___|_|
#                                                            | |   | |
#                                                            |_|   |_|
#                           BY vob#1634 and Anniken#0001


### Imports, do not touch! ###
from __future__ import print_function
from secrets import token
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
from datetime import datetime, timedelta
import secrets
from time import timezone
from sduiapi.packet import Wrapper

print(
    """
    #   _____     _       _  ___  ______ _____   _    _
    #  /  ___|   | |     (_)/ _ \ | ___ \_   _| | |  | |
    #  \ `--.  __| |_   _ _/ /_\ \| |_/ / | |   | |  | |_ __ __ _ _ __  _ __   ___ _ __
    #   `--. \/ _` | | | | |  _  ||  __/  | |   | |/\| | '__/ _` | '_ \| '_ \ / _ \ '__|
    #  /\__/ / (_| | |_| | | | | || |    _| |_  \  /\  / | | (_| | |_) | |_) |  __/ |
    #  \____/ \__,_|\__,_|_\_| |_/\_|    \___/   \/  \/|_|  \__,_| .__/| .__/ \___|_|
    #                                                            | |   | |
    #                                                            |_|   |_|
    #                           BY vob#1634 and Anniken#0001
    """)

### Variables ###

CALENDAR_ID = "primary"
TIME_DELTA = -7

### Code - Do not touch unless you know what you are doing ###


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

Wrapper = Wrapper(TOKEN=token, TABLE_ID=305870)


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=20, singleEvents=True,
                                          orderBy='startTime').execute()
    eventsToday = events_result.get('items', [])

    data = Wrapper.get_lessons_for_day(TIME_DELTA)

    for i in data:
        if "oftype" in i:
            if i["oftype"] == "SUB":
                name = i["subject"]
                desc = "New Teacher: " + i["teacher"]
                color = 4
            elif i["oftype"] == "CANCLED":
                name = "Free."
                color = 8
            elif i["oftype"] == "ROOM_CHANGE":
                name = i["subject"]
                desc = "Room was changed."
                color = 5
        else:
            desc = ""
            color = 1
            name = i["subject"]
        event = create_event(i["begin"], i["end"], name, desc, service, colorId=color)
        print('Event created: %s' % (event.get('htmlLink')))


def create_event(time_start, time_end, name, desc, service_handler, colorId):
    time_with_delta = datetime.now() - timedelta(TIME_DELTA)

    formdate = '-'.join(str(time_with_delta.strftime("%Y-%D-%M")
                            ).replace("/", "-").split("-")[0:3])

    GMT_OFF = '+02:00'

    EVENT = {
        'summary': name,
        'colorId': colorId,
        "description": desc,
        'start': {'dateTime': formdate + "T" + str(timedelta(seconds=time_start+60*60)) + GMT_OFF},
        'end': {'dateTime': formdate + "T" + str(timedelta(seconds=time_end+60*60)) + GMT_OFF},
    }

    event = service_handler.events().insert(
        calendarId=CALENDAR_ID, body=EVENT).execute()
    return event


if __name__ == '__main__':
    main()
