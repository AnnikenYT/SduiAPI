import requests
import secrets
import json

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

    lessons = {}

    jdata = prepare_json_data(jdata)

    for i in jdata["data"]["lessons"]:

        try:
            ni = jdata["data"]["lessons"][i]
            lessons[i] = [ni["teachers"][0]["name"], ni["teachers"][0]["id"], ni["course"]["meta"]["displayname"]]

        except Exception as e:
            print("(Mild) Error at " + str(i))

    return lessons

