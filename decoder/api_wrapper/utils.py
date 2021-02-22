import json
import requests


def read_json_file(json_file):
    with open(json_file, encoding='utf8') as f:
        return json.load(f)


def get_card_set_online(set_num: int, region="en_us"):
    url = f'http://dd.b.pvp.net/latest/set{set_num}/{region}/data/set{set_num}-{region}.json'
    print('Loading: ', url)
    r = requests.get(url)
    return r.json()


def get_lor_globals(region="en_us"):
    url = f"https://dd.b.pvp.net/latest/core/{region}/data/globals-{region}.json"
    print('Loading: ', url)
    r = requests.get(url)
    return r.json()