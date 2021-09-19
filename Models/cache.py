import json
import os

class Cache():
    
    def __init__(self) -> None:
        self.matchDetails = {}
        self.riotIds = {}
        self.playerNames = {}
        self.matches = {}

    def loadJson(self):
        try:
            with open('data/matchDetails.json', 'r', encoding='utf-8') as fp:
                self.matchDetails = json.load(fp)
            with open('data/riotIds.json', 'r', encoding='utf-8') as fp:
                self.riotIds = json.load(fp)
            with open('data/playerNames.json', 'r', encoding='utf-8') as fp:
                self.playerNames = json.load(fp)
            with open('data/matches.json', 'r', encoding='utf-8') as fp:
                self.matches = json.load(fp)
        except Exception as e:
            print('loadJson error', e)
            return

    def save(self):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/matchDetails.json', 'w+', encoding='utf-8') as fp:
                json.dump(self.matchDetails, fp, ensure_ascii=False, indent=2)
            with open('data/riotIds.json', 'w+', encoding='utf-8') as fp:
                json.dump(self.riotIds, fp, ensure_ascii=False, indent=2)
            with open('data/playerNames.json', 'w+', encoding='utf-8') as fp:
                json.dump(self.playerNames, fp, ensure_ascii=False, indent=2)
        except Exception as e:
            print('save cache error: ', e)
            return