import json
import os
import constants

class Cache():
    
    def __init__(self) -> None:
        self.matchDetails = {}
        self.riotIds = {}
        self.playerNames = {}
        self.matches = {}

    def loadJson(self):
        try:
            with open(constants.getCacheFilePath('matchDetails.json'), 'r', encoding='utf-8') as fp:
                self.matchDetails = json.load(fp)
            with open(constants.getCacheFilePath('riotIds.json'), 'r', encoding='utf-8') as fp:
                self.riotIds = json.load(fp)
            with open(constants.getCacheFilePath('playerNames.json'), 'r', encoding='utf-8') as fp:
                self.playerNames = json.load(fp)
            with open(constants.getCacheFilePath('matches.json'), 'r', encoding='utf-8') as fp:
                self.matches = json.load(fp)
        except Exception as e:
            print('loadJson error', e)
            return

    def save(self):
        try:
            with open(constants.getCacheFilePath('matchDetails.json'), 'w+', encoding='utf-8') as fp:
                json.dump(self.matchDetails, fp, ensure_ascii=False, indent=2)
            with open(constants.getCacheFilePath('riotIds.json'), 'w+', encoding='utf-8') as fp:
                json.dump(self.riotIds, fp, ensure_ascii=False, indent=2)
            with open(constants.getCacheFilePath('playerNames.json'), 'w+', encoding='utf-8') as fp:
                json.dump(constants.getCacheFilePath('matches.json'), fp, ensure_ascii=False, indent=2)
        except Exception as e:
            print('save cache error: ', e)
            return