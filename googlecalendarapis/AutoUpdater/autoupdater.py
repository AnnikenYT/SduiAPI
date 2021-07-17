from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from colorama import Fore, Back, Style

from datetime import datetime, timedelta

import time

import packet, secrets

# The script needs userinfo.profile, for auth
SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.profile']

def create_event(time_start, time_end, name, service_handler, colorId=7):

    formdate = '-'.join(str(datetime.now().strftime("%Y-%D-%M")).replace("/", "-").split("-")[0:3])

    GMT_OFF = '+02:00'


    GMT_OFF = '+02:00'
    EVENT = {
        'summary': name,
        'colorId':colorId,
        'start': {'dateTime': formdate + "T" + str(timedelta(seconds=time_start+60*60)) + GMT_OFF},
        'end': {'dateTime': formdate + "T" + str(timedelta(seconds=time_end+60*60)) + GMT_OFF},
    }


    event = service_handler.events().insert(calendarId='primary', body=EVENT).execute()

def minute_passed(oldepoch):
    return time.time() - oldepoch >= 60*60


def main():

    sduiPackage = packet.Wrapper(TABLE_ID=305516, TIME_DELTA=0, TOKEN=secrets.token)

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

    last_epoch = time.time()

    firstrun = True

    while True:
        if minute_passed(last_epoch) or firstrun:
            last_epoch = time.time()
            lessons = sduiPackage.get_lessons_for_day(3)
            combilist = []
            combilist_timesort = []

            

            for i in lessons[0]:
                combilist.append(i)

            for i in lessons[1]:
                flag = False

                for ix in combilist:
                    if ix["subject"] == i["subject"]:
                        try:
                            ix["oftype"]
                        except:
                            pass
                        else:
                            flag=True
                if not flag:
                    combilist.append(i)

            

            combilist = sorted(combilist, key=lambda x: x["beginn"])


            for i in combilist:
                t=0
                try: i["oftype"]
                except:

                    t+=1
                    print(Fore.BLACK + Style.BRIGHT + Back.LIGHTGREEN_EX +
                                "[ HOUR " + str(t) + " ]" + " ✔ Unchanged: " + Style.RESET_ALL)
                    print(Fore.BLACK + Style.BRIGHT + Back.LIGHTGREEN_EX +
                                " |-> " + i["subject"]   + Style.RESET_ALL)

                    create_event(i["beginn"], i["end"], i["subject"], service)

                else:
                    t += 1
                    if i["oftype"] == "SUB":
                        print(Fore.WHITE + Style.BRIGHT + Back.RED + "[ HOUR " + str(t) + " ]" + " ✖ Changed: " + Style.RESET_ALL)
                        print(Fore.BLACK + Style.BRIGHT + Back.CYAN + " |->" + i["subject"] + Style.RESET_ALL)
                        print(Fore.BLACK + Style.BRIGHT + Back.CYAN + "   |--> To Teacher " + i["teacher"] + Style.RESET_ALL)

                        create_event(i["beginn"], i["end"], i["subject"] + " --- Sub Teacher " + i["teacher"], service, colorId=4)



                    elif i['oftype'] == "CANCLED":
                        print(Fore.WHITE + Style.BRIGHT + Back.RED + "[ HOUR " + str(t) + " ]" + " ✖ Cancled: " + Style.RESET_ALL)
                        print(Fore.WHITE + Style.BRIGHT + Back.LIGHTBLACK_EX + " |-> " + i["subject"] + " Cancled!" + Style.RESET_ALL)

                        create_event(i["beginn"], i["end"], i["subject"] + " Cancled!", service, colorId=11)
                    
                    elif i["oftype"] == "CHANGE":
                        print(Fore.WHITE + Style.BRIGHT + Back.RED + "[ HOUR " + str(t) + " ]" + " ✖ Changed: " + Style.RESET_ALL)
                        print(Fore.BLACK + Style.BRIGHT + Back.CYAN + " |->" + i["subject"] + Style.RESET_ALL)
                        print(Fore.BLACK + Style.BRIGHT + Back.MAGENTA + "  |--> To Room " + i["room"] + Style.RESET_ALL)
                        create_event(i["beginn"], i["end"], i["subject"] + " --- New Room " + i["room"], service,colorId=3)
        
                t=0
                firstrun = False

if __name__ == '__main__':
    main()