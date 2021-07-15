from main import DEBUG, MAX_DATA_LIFETIME, TABLE_ID, TIME_DELTA
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


def cleanlist(lst):
    fixed_list = []
    broken_list = []

    for i in lst:
        if str(i) not in broken_list and i != []:
            broken_list.append(str(i))
            fixed_list.append(i)

    print(fixed_list)
    
    return fixed_list

class SduiAPI:

    TABLE_ID = 0
    TIME_DELTA = 0
    MAX_DATA_LIFETIME = 3600
    DEBUG = False

    def __init__(self, tableid, timedelta=0, maxdatalifetime=3600, debug=False) -> None:
        TABLE_ID = tableid
        TIME_DELTA = timedelta
        MAX_DATA_LIFETIME = maxdatalifetime
        DEBUG = debug

    def get_lessons_for_day(self, datetoday: datetime):

        TABLE_ID = self.TABLE_ID
        TIME_DELTA = self.TIME_DELTA
        MAX_DATA_LIFETIME = self.MAX_DATA_LIFETIME
        DEBUG = self.DEBUG

        """
        Get lessons for a specific day
        """
        print(Fore.CYAN + Style.BRIGHT +
            f"Checking lessons for {datetoday.date()+timedelta(1)}" + Style.RESET_ALL)
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
                                        skip.append({"subject":targets["subject"]["meta"]["displayname"], "oftype":"SUB", "teacher":targets["teachers"][0]["name"],"beginn":targets["time_begins_at"], "end":targets["time_ends_at"],})
                                    elif targets["kind"] == "CANCLED":
                                        skip.append({"subject":targets["course"]["meta"]["displayname"], "oftype":"CANCLED", "beginn":targets["time_begins_at"], "end":targets["time_ends_at"]})
                                    else:
                                        pass
                    if DEBUG:
                        print(Fore.BLACK + Style.DIM +
                            f"Checking date: {lessondate} against today's date {checkdate}" + Style.RESET_ALL)
                    if lessondate == checkdate:
                        print(Fore.BLACK + Style.BRIGHT + Back.GREEN +
                            "✔ Found: " + Style.RESET_ALL)
                        print(Fore.BLACK + Style.BRIGHT + Back.GREEN +
                            lessons[i]["meta"]["displayname"] + Style.RESET_ALL)
                        
                        found.append({"subject":lessons[i]["meta"]["displayname"], "begin":lessons[i]["time_begins_at"], "end":lessons[i]["time_ends_at"]})

                    else:
                        if DEBUG:
                            print(Fore.BLACK + Style.BRIGHT + Back.RED +
                                "✖ Nothing Found" + Style.RESET_ALL)
                        else:
                            pass

                    for i_ in skip:
                        if str(i_) != str('[]'):
                            pass

        return [cleanlist(skip), found]