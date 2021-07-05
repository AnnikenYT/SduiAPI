import requests
import secrets
import json

### TABLES: AnnikenYT:305870 BigBoy32:305516

def get_data(target_table):
    url = f'https://api.sdui.app/v1/users/{target_table}/timetable'
    headers = {
        "authorization": secrets.token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    json.dump(r.json(), open("data.json", "w"))

get_data()