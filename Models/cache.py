import json
import os
import constants


class Cache():

    def __init__(self) -> None:
        self.matchDetails = {}
        self.riotIds = {}
        self.playerNames = {}
        self.matches = {}
        self.localMatches = {}
        self.loadJson()

    def loadJson(self):
        try:
            with open(constants.getCacheFilePath('matchDetails.json'), 'r', encoding='utf-8') as fp:
                self.matchDetails = json.load(fp)
        except Exception as e:
            print('loadJson matchDetails error', e)
        try:
            with open(constants.getCacheFilePath('riotIds.json'), 'r', encoding='utf-8') as fp:
                self.riotIds = json.load(fp)
        except Exception as e:
            print('loadJson riotIds error', e)
        try:
            with open(constants.getCacheFilePath('playerNames.json'), 'r', encoding='utf-8') as fp:
                self.playerNames = json.load(fp)
        except Exception as e:
            print('loadJson playerNames error', e)
        try:
            with open(constants.getCacheFilePath('matches.json'), 'r', encoding='utf-8') as fp:
                self.matches = json.load(fp)
        except Exception as e:
            print('loadJson matches error', e)
        try:
            with open(constants.getCacheFilePath('localMatches.json'), 'r', encoding='utf-8') as fp:
                self.localMatches = json.load(fp)
        except Exception as e:
            print('loadJson localMatches error', e)  

    def save(self):
        try:
            with open(constants.getCacheFilePath('matchDetails.json'), 'w+', encoding='utf-8') as fp:
                json.dump(self.matchDetails, fp, ensure_ascii=False, indent=2)
            with open(constants.getCacheFilePath('riotIds.json'), 'w+', encoding='utf-8') as fp:
                json.dump(self.riotIds, fp, ensure_ascii=False, indent=2)
            with open(constants.getCacheFilePath('playerNames.json'), 'w+', encoding='utf-8') as fp:
                json.dump(self.playerNames, fp, ensure_ascii=False, indent=2)
            with open(constants.getCacheFilePath('matches.json'), 'w+', encoding='utf-8') as fp:
                json.dump(self.matches, fp, ensure_ascii=False, indent=2)
        except Exception as e:
            print('save cache error: ', e)

    def saveLocal(self):
        try:
            with open(constants.getCacheFilePath('localMatches.json'), 'w+', encoding='utf-8') as fp:
                json.dump(self.localMatches, fp, ensure_ascii=False, indent=2)
        except Exception as e:
            print('save cache error: ', e)
