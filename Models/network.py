import random
import urllib.request

API_KEY1 = '?api_key=' + 'ADD YOUR API KEY HERE'

MATCH_KEY = '.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = '.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PUUID_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

allKeys = [API_KEY1]
random.shuffle(allKeys)
API_KEY = allKeys[0]
aviliableKeys = []


def switchAPI():
    global aviliableKeys
    if not aviliableKeys:
        aviliableKeys = allKeys.copy()
    global API_KEY
    random.shuffle(aviliableKeys)
    API_KEY = aviliableKeys.pop()


def getProxy():
    return urllib.request.getproxies()


class Network():
    def __init__(self, setting) -> None:
        self.setting = setting
        self.key = API_KEY
        return

    def getHeadLink(self):
        return 'https://' + self.setting.riotServer

    def getMatchesLink(self, ppid):
        return self.getHeadLink() + MATCH_KEY + ppid + '/ids' + API_KEY

    def getDetailsLink(self, matchId):
        return self.getHeadLink() + DETAILS_KEY + matchId + API_KEY

    def getNameLink(self, ppid):
        return self.getHeadLink() + NAME_KEY + ppid + API_KEY

    def getPUUID(self, name, tag):
        return self.getHeadLink() + PUUID_KEY + name + '/' + tag + API_KEY
