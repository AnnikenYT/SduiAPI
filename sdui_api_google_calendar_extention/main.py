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
from sdui_api.classes import Cancled, Lesson, RoomChange, Substitution
from secrets import token
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
from datetime import datetime, timedelta
import secrets
from time import timezone
from sdui_api.wrapper import Wrapper

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
TIME_DELTA = -1
TABLE_ID = ""

LESSON_COLOR = "blue"
SUBSTITUTION_COLOR = "orange"
CANCLED_COLOR = "red"
ROOMCHANGE_COLOR = "turquoise"

### Code - Do not touch unless you know what you are doing ###


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

wrp = Wrapper(TOKEN=token, TABLE_ID=TABLE_ID)

dir = os.path.dirname(__file__)

def main():
    """
    The main code to add all events using the API Wrapper package
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(dir + '\\token.json'):
        creds = Credentials.from_authorized_user_file(dir + '\\token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                dir + '\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(dir + '\\token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=20, singleEvents=True,
                                          orderBy='startTime').execute()
    eventsToday = events_result.get('items', [])

    # data = Wrapper.get_lessons_for_day(TIME_DELTA)

    # for i in data:
    #     if "oftype" in i:
    #         if i["oftype"] == "SUB":
    #             name = i["subject"]
    #             desc = "New Teacher: " + i["teacher"]
    #             color = 4
    #         elif i["oftype"] == "CANCLED":
    #             name = "Free."
    #             color = 8
    #         elif i["oftype"] == "ROOM_CHANGE":
    #             name = i["subject"]
    #             desc = "Room was changed."
    #             color = 5
    #     else:
    #         desc = ""
    #         color = 1
    #         name = i["subject"]

    lessons = wrp.get_lessons_for_day(TIME_DELTA)
    for lesson in lessons:
        desc = f"""
        Room: {lesson.getRoom(1).shortcut},
        Teacher: {lesson.getTeacher(1).name}
        """
        color = LESSON_COLOR
        if type(lesson) is Substitution:
            color = SUBSTITUTION_COLOR
        elif type(lesson) is Cancled:
            color = CANCLED_COLOR
            desc = f"""
            Lesson is cancled
            """
        elif type(lesson) is RoomChange:
            color = ROOMCHANGE_COLOR
        event = create_event(lesson.begin, lesson.end, lesson.name, desc, service, colorId=convertColorCode(color))
        print('Event created: %s' % (event.get('htmlLink')))

def convertColorCode(color: str):
    colors = {
        "blue": 1,
        "green": 2,
        "purple": 3,
        "red": 4,
        "yellow": 5,
        "orange": 6,
        "turquoise": 7,
        "gray": 8,
    }
    try:
        return colors[color]
    except:
        print(f"Couldnt find color '{color}', returning default of 'blue'")
        return 1

def create_event(time_start, time_end, name, desc, service_handler, colorId):
    """
    Add an event using the google calendar api
    """
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
