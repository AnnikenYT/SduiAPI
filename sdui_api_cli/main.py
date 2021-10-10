
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
TIME_DELTA = -1
MAX_DATA_LIFETIME = 3600
DEBUG = False

### Code - Do not touch, unless you know what your doing ###

from itertools import repeat, chain


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
    //@BigBoy32 Here. Here we are unziping the data, and getting the teacher map
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

def cleanlist(lst):
    fixed_list = []
    broken_list = []

    for i in lst:
        if str(i) not in broken_list and i != []:
            broken_list.append(str(i))
            fixed_list.append(i)

    print(fixed_list)
    
    return fixed_list

def get_lessons_for_day(datetoday: datetime):
    """
    Get lessons for a specific day
    """
    print(Fore.CYAN + Style.BRIGHT +
          f"Checking lessons for {datetoday.date()+timedelta(1)}" + Style.RESET_ALL)
    try:
        jdata = load_data()
        lessons = jdata["data"]["lessons"]
    except:
        print(Fore.RED + "Something seems to be wrong with your JSON file. Redownloading..." + Style.RESET_ALL)
        os.remove("LAST_DOWNLOAD")
        jdata = load_data()
        lessons = jdata["data"]["lessons"]

    skip = []
    found = []

    for i in lessons:
        if lessons[i] is not None:
            
            for d in lessons[i]["dates"]:
                unixtoday = dt2unix(datetoday)
                checkdate = unixtoday
                lessondate = d

                if lessons[i]["substituted_target_lessons"] != []:
                    for targets in lessons[i]["substituted_target_lessons"]:
                        for targetdate in targets["dates"]:
                            if targetdate == checkdate:
                                if targets["kind"] == "SUBSTITUTION":
                                    skip.append({"subject":targets["subject"]["meta"]["displayname"], "oftype":"SUB", "teacher":targets["teachers"][0]["name"],"begin":targets["time_begins_at"], "end":targets["time_ends_at"],})
                                elif targets["kind"] == "CANCLED":
                                    skip.append({"subject":targets["course"]["meta"]["displayname"], "oftype":"CANCLED", "begin":targets["time_begins_at"], "end":targets["time_ends_at"]})
                                elif targets["kind"] == "BOOKABLE_CHANGE":
                                    skip.append({"subject":targets["course"]["meta"]["displayname"], "oftype":"CHANGE", "begin":targets["time_begins_at"], "end":targets["time_ends_at"], "room":targets["bookables"][0]["shortcut"]})
                                else:
                                    pass

                    else:
                        pass

                for i_ in skip:
                    if str(i_) != str('[]'):
                        pass

                if lessondate == checkdate:
                    flag = False
                    for __i in skip:
                        if __i["subject"] == lessons[i]["meta"]["displayname"]:
                            flag = True
                        else:
                            pass
                    if not flag:
                        found.append({"subject":lessons[i]["meta"]["displayname"], "begin":lessons[i]["time_begins_at"], "end":lessons[i]["time_ends_at"]})


    return [cleanlist(skip), found]

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

def cli_text():

    data = get_lessons_for_day(datetoday=datetime.now().replace(
    hour=22, minute=0, second=0)-timedelta(TIME_DELTA+1))

    skip = data[0]
    unchanged = data[1]

    combilist = []
    combilist_timesort = []

    for i in skip:
        combilist.append(i)
    
    for i in unchanged:
        combilist.append(i)

    combilist = sorted(combilist, key=lambda x: x["begin"])
    
    t = 0

    for i in combilist:
        try: i["oftype"]
        except:

            t+=1
            print(Fore.BLACK + Style.BRIGHT + Back.LIGHTGREEN_EX +
                          "[ HOUR " + str(t) + " ]" + " ✔ Unchanged: " + Style.RESET_ALL)
            print(Fore.BLACK + Style.BRIGHT + Back.LIGHTGREEN_EX +
                        " |-> " + i["subject"]   + Style.RESET_ALL)

        else:
            t += 1
            if i["oftype"] == "SUB":
                print(Fore.WHITE + Style.BRIGHT + Back.RED + "[ HOUR " + str(t) + " ]" + " ✖ Changed: " + Style.RESET_ALL)
                print(Fore.BLACK + Style.BRIGHT + Back.CYAN + " |->" + i["subject"] + Style.RESET_ALL)
                print(Fore.BLACK + Style.BRIGHT + Back.CYAN + "   |--> To Teacher " + i["teacher"] + Style.RESET_ALL)

            elif i['oftype'] == "CANCLED":
                print(Fore.WHITE + Style.BRIGHT + Back.RED + "[ HOUR " + str(t) + " ]" + " ✖ Cancled: " + Style.RESET_ALL)
                print(Fore.WHITE + Style.BRIGHT + Back.LIGHTBLACK_EX + " |-> " + i["subject"] + " Cancled!" + Style.RESET_ALL)
            
            elif i["oftype"] == "CHANGE":
                print(Fore.WHITE + Style.BRIGHT + Back.RED + "[ HOUR " + str(t) + " ]" + " ✖ Changed: " + Style.RESET_ALL)
                print(Fore.BLACK + Style.BRIGHT + Back.CYAN + " |->" + i["subject"] + Style.RESET_ALL)
                print(Fore.BLACK + Style.BRIGHT + Back.MAGENTA + "  |--> To Room " + i["room"] + Style.RESET_ALL)
    """
    for it in unchanged:
        print(Fore.BLACK + Style.BRIGHT + Back.GREEN +
                          "✔ Unchanged: " + Style.RESET_ALL)
        print(Fore.BLACK + Style.BRIGHT + Back.GREEN +
                        "|->" + it["subject"]   + Style.RESET_ALL)
    
    for sk in skip:
        if sk["oftype"] == "SUB":
            print(Fore.WHITE + Style.BRIGHT + Back.RED + "✖ Changed: " + Style.RESET_ALL)
            print(Fore.BLACK + Style.BRIGHT + Back.CYAN + "|->" + sk["subject"] + Style.RESET_ALL)
            print(Fore.BLACK + Style.BRIGHT + Back.CYAN + "|--> To Teacher " + sk["teacher"] + Style.RESET_ALL)

    """
cli_text()
