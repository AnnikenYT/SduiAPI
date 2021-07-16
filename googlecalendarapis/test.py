from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from datetime import datetime, timedelta

# The script needs userinfo.profile, for auth
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.profile']

def create_event(time_start, time_end, name, service_handler):

    formdate = '-'.join(str(datetime.now().strftime("%Y-%D-%M")).replace("/", "-").split("-")[0:3])

    GMT_OFF = '+02:00'

    print(formdate + "T" + str(timedelta(seconds=time_start)) + GMT_OFF)

    GMT_OFF = '+02:00'
    EVENT = {
        'summary': 'Sample',
        'start': {'dateTime': formdate + "T" + str(timedelta(seconds=time_start)) + GMT_OFF},
        'end': {'dateTime': formdate + "T" + str(timedelta(seconds=time_end)) + GMT_OFF},
    }


    event = service_handler.events().insert(calendarId='primary', body=EVENT).execute()

    print("Created Event for:", name)


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

    create_event(35000, 37000, "Test Event", service)

if __name__ == '__main__':
    main()