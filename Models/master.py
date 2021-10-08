import json
import requests
import constants
import threading
import time
from Models.setting import Server

session = requests.Session()


def get_playernames(server):
    url = f"https://raw.githubusercontent.com/LoR-Master-Tracker/LoR-Player-Crawler/master/save/{server}.json"
    print('Loading: ', url)
    r = session.get(url)

    # valid json:
    try:
        jsonObject = r.json()
    except Exception as e:
        print(url, 'Json valid issue: ', e)
        return
    with open(constants.getCacheFilePath(server.lower() + '.json'), 'w', encoding='utf-8') as fp:
        json.dump(jsonObject, fp, ensure_ascii=False, indent=2)


def getAllList():
    while True:
        for server in list(Server):
            try:
                get_playernames(server.value)
            except Exception as e:
                print('Model.master error: ', e)
        time.sleep(3600)

def startMasterWorker():
    n = threading.Thread(target=getAllList)
    n.daemon = True
    n.start()
