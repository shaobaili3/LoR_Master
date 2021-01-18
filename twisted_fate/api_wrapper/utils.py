import json
import requests

def read_json_file(json_file):
    with open(json_file,encoding='utf8') as f:
        return json.load(f)


def get_card_set_online(set_num: int, region="en_us"):
    url = f"https://raw.githubusercontent.com/pedrofracassi/lor-bundles/master/set{set_num}/{region}/data/set{set_num}-{region}.json"
    r = requests.get(url)   
    return r.json()


def get_lor_globals(region="en_us"):
    url = f"https://raw.githubusercontent.com/pedrofracassi/lor-bundles/master/core/{region}/data/globals-{region}.json"
    r = requests.get(url)
    return r.json()