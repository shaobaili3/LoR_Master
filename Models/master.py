import json
import requests
import os
from Models.setting import Server


session = requests.Session()

def read_json_file(json_file):
    with open(json_file, encoding='utf8') as f:
        return json.load(f)

def get_playernames(server):
    url = f"https://raw.githubusercontent.com/LoR-Master-Tracker/LoR-Player-Crawler/master/{server}.json"
    print('Loading: ', url)
    r = session.get(url)
    os.makedirs('data', exist_ok=True)
    with open('data/' + server +'.json', 'w+', encoding='utf-8') as fp:
        json.dump(r.json(), fp, ensure_ascii=False, indent= 2)


get_playernames(Server.NA)
get_playernames(Server.EU)
get_playernames(Server.ASIA)