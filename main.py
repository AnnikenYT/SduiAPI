import requests
import secrets
import json

from datetime import datetime

def unix2dt(ts):
    print(datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S'))

### TABLES: AnnikenYT:305870 BigBoy32:305516

def prepare_json_data(jdata):
    if jdata == None:
        return json.load(open("data.json", "r"))
    else:
        return jdata

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

    jdata = prepare_json_data(jdata)

    try:
        for i in jdata["data"]["lessons"]:
            
            ni = jdata["data"]["lessons"][i]

            dmap = []

            this_teacher = ni["teachers"][0]["shortcut"]

            try:
                for i in teacher_map[this_teacher]:
                    dmap.append(i)

            except: pass

            for i in ni["dates"]:
                dmap.append(i)

            dates = dmap

            class_name = ni["meta"]["displayname"]

            teacher_map[this_teacher] = [dates, class_name]
    except:
        pass

    return teacher_map

print(get_lessons())
