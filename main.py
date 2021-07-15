
#   _____     _       _  ___  ______ _____   _    _                                 
#  /  ___|   | |     (_)/ _ \ | ___ \_   _| | |  | |                                
#  \ `--.  __| |_   _ _/ /_\ \| |_/ / | |   | |  | |_ __ __ _ _ __  _ __   ___ _ __ 
#   `--. \/ _` | | | | |  _  ||  __/  | |   | |/\| | '__/ _` | '_ \| '_ \ / _ \ '__|
#  /\__/ / (_| | |_| | | | | || |    _| |_  \  /\  / | | (_| | |_) | |_) |  __/ |   
#  \____/ \__,_|\__,_|_\_| |_/\_|    \___/   \/  \/|_|  \__,_| .__/| .__/ \___|_|   
#                                                            | |   | |              
#                                                            |_|   |_|              
#                           BY vob#1634 and Anniken#0001


import requests
import secrets
import json
import calendar
import time
from colorama import Fore, Back, Style
from datetime import datetime, date, timedelta



def unix2dt(ts):
    return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

def dt2unix(dt):
    return calendar.timegm(dt.utctimetuple())

### TABLES: AnnikenYT:305870 BigBoy32:305516

def load_data():
    return json.load(open("data.json", "r"))

def get_data(target_table):
    url = f'https://api.sdui.app/v1/users/{str(target_table)}/timetable'
    headers = {
        "authorization": secrets.token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    json.dump(r.json(), open("data.json", "w"))

def get_lessons(jdata=None):

    teacher_map = {}

    jdata = load_data()

    try:
        for i in jdata["data"]["lessons"]:
            
            ni = jdata["data"]["lessons"][i]

            dmap = []

            this_teacher = ni["teachers"][0]["shortcut"]

            try:
                for y in teacher_map[this_teacher]:
                    dmap.append(unix2dt(y))

            except: pass

            for i in ni["dates"]:
                dmap.append(unix2dt(i))

            dates = dmap

            class_name = ni["meta"]["displayname"]

            teacher_map[this_teacher] = [dates, class_name]
    except:
        pass

    return teacher_map

def get_lessons_today():
    jdata = load_data()
    lessons = jdata["data"]["lessons"]
    for i in lessons:
        if lessons[i] is not None:
            for d in lessons[i]["dates"]:
                datetoday = datetime.now().replace(hour=22, minute=0, second=0)-timedelta(3)
                unixtoday = dt2unix(datetoday)
                checkdate = unixtoday
                lessondate = d
                #print(Fore.BLACK + Style.DIM + f"Checking date: {lessondate} against today's date {checkdate}" + Style.RESET_ALL)
                if lessondate == checkdate:
                    print(Fore.BLACK + Style.BRIGHT + Back.GREEN + "✔ Found: " + Style.RESET_ALL)
                    print(Fore.BLACK + Style.BRIGHT + Back.GREEN + lessons[i]["meta"]["displayname"] + Style.RESET_ALL)
                #else:
                    #print(Fore.BLACK + Style.BRIGHT + Back.RED + "✖ Nothing Found" + Style.RESET_ALL)
                    
get_lessons_today()