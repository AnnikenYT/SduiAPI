
#   _____     _       _  ___  ______ _____   _    _
#  /  ___|   | |     (_)/ _ \ | ___ \_   _| | |  | |
#  \ `--.  __| |_   _ _/ /_\ \| |_/ / | |   | |  | |_ __ __ _ _ __  _ __   ___ _ __
#   `--. \/ _` | | | | |  _  ||  __/  | |   | |/\| | '__/ _` | '_ \| '_ \ / _ \ '__|
#  /\__/ / (_| | |_| | | | | || |    _| |_  \  /\  / | | (_| | |_) | |_) |  __/ |
#  \____/ \__,_|\__,_|_\_| |_/\_|    \___/   \/  \/|_|  \__,_| .__/| .__/ \___|_|
#                                                            | |   | |
#                                                            |_|   |_|
#                           BY vob#1634 and Anniken#0001

### Variables ###

TABLE_ID = 305870
TIME_DELTA = 1
MAX_DATA_LIFETIME = 3600
DEBUG = False

### Code - Do not touch, unless you know what your doing ###

import os
from datetime import datetime, date, timedelta
from colorama import Fore, Back, Style
import time
import calendar
import json
import secrets
import requests

def unix2dt(ts):
    """
    Convert unix timestamp to datetime
    """
    return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


def dt2unix(dt):
    """
    Convert datetime to unix timestamp
    """
    return calendar.timegm(dt.utctimetuple())

# TABLES: AnnikenYT:305870 BigBoy32:305516


def load_data():
    """
    Load data from downloaded data
    """
    if not os.path.exists('LAST_DOWNLOAD'):
        get_data(TABLE_ID)
    with open("LAST_DOWNLOAD", "r") as file:
        last_download = file.read()
        if last_download.strip() != "":
            last_download = unix2dt(last_download)
            last = datetime.strptime(last_download, "%Y-%m-%d %H:%M:%S")
            diff = datetime.now() - last
            if diff.total_seconds() >= MAX_DATA_LIFETIME:
                get_data(TABLE_ID)
                return json.load(open("data.json", "r"))
            else:
                return json.load(open("data.json", "r"))
        else:
            get_data(TABLE_ID)
            return json.load(open("data.json", "r"))


def get_data(target_table):
    """
    Download data to file
    """
    with open("LAST_DOWNLOAD", "w+") as file:
        file.seek(0)
        file.write(str(dt2unix(datetime.now())))
    print(Fore.RED + "Data too old, downloading new data." + Style.RESET_ALL)
    url = f'https://api.sdui.app/v1/users/{str(target_table)}/timetable'
    headers = {
        "authorization": secrets.token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    json.dump(r.json(), open("data.json", "w+"))


def get_lessons():
    """
    ???
    //TODO @BigBoy32 Add description please.
    """
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

            except:
                pass

            for i in ni["dates"]:
                dmap.append(unix2dt(i))

            dates = dmap

            class_name = ni["meta"]["displayname"]

            teacher_map[this_teacher] = [dates, class_name]
    except:
        pass

    return teacher_map


def get_lessons_for_day(datetoday: datetime):
    """
    Get lessons for a specific day
    """
    print(Fore.CYAN + Style.BRIGHT +
          f"Checking lessons for {datetoday.date()+timedelta(1)}" + Style.RESET_ALL)
    jdata = load_data()
    lessons = jdata["data"]["lessons"]
    for i in lessons:
        if lessons[i] is not None:
            for d in lessons[i]["dates"]:
                unixtoday = dt2unix(datetoday)
                checkdate = unixtoday
                lessondate = d
                if DEBUG:
                    print(Fore.BLACK + Style.DIM +
                          f"Checking date: {lessondate} against today's date {checkdate}" + Style.RESET_ALL)
                if lessondate == checkdate:
                    print(Fore.BLACK + Style.BRIGHT + Back.GREEN +
                          "✔ Found: " + Style.RESET_ALL)
                    print(Fore.BLACK + Style.BRIGHT + Back.GREEN +
                          lessons[i]["meta"]["displayname"] + Style.RESET_ALL)
                else:
                    if DEBUG:
                        print(Fore.BLACK + Style.BRIGHT + Back.RED +
                              "✖ Nothing Found" + Style.RESET_ALL)
                    else:
                        pass
        # TODO return array with hours today


get_lessons_for_day(datetoday=datetime.now().replace(
    hour=22, minute=0, second=0)-timedelta(TIME_DELTA+1))
