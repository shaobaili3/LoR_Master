import json
import requests
import os
import threading
import time
from Models.setting import Server

session = requests.Session()

def get_playernames(server):
    url = f"https://raw.githubusercontent.com/LoR-Master-Tracker/LoR-Player-Crawler/master/{server}.json"
    print('Loading: ', url)
    r = session.get(url)

    #valid json:
    try:
        jsonObject = r.json()
    except Exception as e:
        print('Json valid issue: ', e)
        return
    os.makedirs('data', exist_ok=True)
    with open('data/' + server +'.json', 'w+', encoding='utf-8') as fp:
        json.dump(jsonObject, fp, ensure_ascii=False, indent= 2)

def f(s):
    while True:
        try:
            get_playernames(s)
        except Exception as e:
            print('Model.master error: ', e)
        time.sleep(3600)

n = threading.Thread(target=f, args = (Server.NA,))
n.daemon = True 
n.start()

e = threading.Thread(target=f, args = (Server.EU,))
e.daemon = True 
e.start()

a = threading.Thread(target=f, args = (Server.ASIA,))
a.daemon = True 
a.start()