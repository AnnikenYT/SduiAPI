import os
from datetime import datetime, timedelta
from colorama import Fore, Back, Style
import calendar
import json
import requests
from sdui_api import classes


class Wrapper:
    def __init__(self, DEBUG: bool = False, MAX_DATA_LIFETIME: int = 3600, TABLE_ID: int = None, TIME_DELTA: int = 0, TOKEN: str = None):
        """
        Wrapper class

        `DEBUG` enable debugging, default: False

        `MAX_DATA_LIFETIME` max lifetime of data file in seconds, will be automatically re-downloaded, default: 3600

        `TABLE_ID` your table id, default: None

        `TIME_DELTA` difference in data in days, default: 0

        `TOKEN` your bearer token, default: None

        :returns: [[changes to default schedule], []]
        """
        self.DEBUG = DEBUG
        self.MAX_DATA_LIFETIME = MAX_DATA_LIFETIME
        self.TABLE_ID = TABLE_ID
        self.TIME_DELTA = TIME_DELTA
        self.TOKEN = TOKEN

    def unix2dt(self, ts):
        """
        Convert unix timestamp to datetime
        """
        return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

    def dt2unix(self, dt):
        """
        Convert datetime to unix timestamp
        """
        return calendar.timegm(dt.utctimetuple())

    def sec2dt(self, sec):
        return timedelta(seconds=sec)

    def load_data(self):
        """
        Load data from downloaded data
        """
        if not os.path.exists('LAST_DOWNLOAD'):
            self.get_data()
        with open("LAST_DOWNLOAD", "r") as file:
            last_download = file.read()
            if last_download.strip() != "":
                last_download = self.unix2dt(last_download)
                last = datetime.strptime(last_download, "%Y-%m-%d %H:%M:%S")
                diff = datetime.now() - last
                if diff.total_seconds() >= self.MAX_DATA_LIFETIME:
                    self.get_data(self.TABLE_ID)
                    return json.load(open("data.json", "r"))
                else:
                    return json.load(open("data.json", "r"))
            else:
                self.get_data(self.TABLE_ID)
                return json.load(open("data.json", "r"))


    def get_data(self):
        """
        Download data to file
        """
        with open("LAST_DOWNLOAD", "w+") as file:
            file.seek(0)
            file.write(str(self.dt2unix(datetime.now())))
        
        if self.DEBUG: print(Fore.RED + "Data too old, downloading new data." + Style.RESET_ALL)
        url = f'https://api.sdui.app/v1/users/{str(self.TABLE_ID)}/timetable'
        headers = {
            "authorization": self.TOKEN,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        json.dump(r.json(), open("data.json", "w+"))


    def cleanlist(self, lst):
        fixed_list = []
        broken_list = []

        for i in lst:
            if str(i) not in broken_list and i != []:
                broken_list.append(str(i))
                fixed_list.append(i)
        return fixed_list
    
    def mergeList(self, skip, found):
        for i in skip:
            for j in found:
                if i["subject"] == j["subject"] and i["begin"] == j["begin"]:
                    pos = found.index(j)
                    found.remove(j)
                    found.insert(pos, i)
        return found


    def get_lessons_for_day(self, delta: int = 0):
        """
        Get lessons for a specific day
        """
        self.TIME_DELTA = delta
        datetoday=datetime.now().replace(
        hour=22, minute=0, second=0)-timedelta(self.TIME_DELTA+1)
        if self.DEBUG:
            print(Fore.CYAN + Style.BRIGHT +
                f"Checking lessons for {datetoday.date()+timedelta(1)}" + Style.RESET_ALL)
        try:
            jdata = self.load_data()
            lessons = jdata["data"]["lessons"]
        except:
            print(Fore.RED + "Something seems to be wrong with your JSON file. Redownloading..." + Style.RESET_ALL)
            os.remove("LAST_DOWNLOAD")
            jdata = self.load_data()
            lessons = jdata["data"]["lessons"]
        skip = []
        found = []

        for lesson in lessons:
            if lesson is not None:
                for date in lesson["dates"]:
                    checkdate = self.dt2unix(datetoday)
                    lessondate = date

                    if lesson["substituted_target_lessons"] != []:
                        for targets in lesson["substituted_target_lessons"]:
                            for targetdate in targets["dates"]:
                                if targetdate == checkdate:
                                    if targets["kind"] == "SUBSTITUTION":
                                        skip.append(classes.Substitution(targets))
                                        # skip.append({"subject":targets["subject"]["meta"]["displayname"], "oftype":"SUB", "teacher":targets["teachers"][0]["name"],"begin":targets["time_begins_at"], "end":targets["time_ends_at"],})
                                    elif targets["kind"] == "CANCLED":
                                        skip.append({"subject":targets["course"]["meta"]["displayname"], "oftype":"CANCLED", "begin":targets["time_begins_at"], "end":targets["time_ends_at"]})
                                    elif targets["kind"] == "BOOKABLE_CHANGE":
                                        skip.append({"subject":targets["course"]["meta"]["displayname"], "oftype":"ROOM_CHANGE", "begin":targets["time_begins_at"], "end":targets["time_ends_at"]})
                                    else:
                                        pass
                    if self.DEBUG:
                        print(Fore.BLACK + Style.DIM +
                            f"Checking date: {lessondate} against today's date {checkdate}" + Style.RESET_ALL)
                    if lessondate == checkdate:
                        found.append(classes.Lesson(lesson))
                        # found.append({"subject":lessons[i]["meta"]["displayname"], "begin":lessons[i]["time_begins_at"], "end":lessons[i]["time_ends_at"]})

                    else:
                        if self.DEBUG:
                            print(Fore.BLACK + Style.BRIGHT + Back.RED +
                                "✖ Nothing Found" + Style.RESET_ALL)

        return self.mergeList(self.cleanlist(skip), found)
