API_KEY = '?api_key=' + 'RGAPI-3dd1641a-6d80-458d-9fb5-357253d7674b'
MATCH_KEY = '.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = '.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PUUID_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

class Network():
    def __init__(self, setting) -> None:
        self.setting = setting
        return

    def getHeadLink(self):
        return 'https://' + self.setting.getServer()

    def getMatchsLink(self, ppid):
        return self.getHeadLink() + MATCH_KEY  + ppid + '/ids' + API_KEY

    def getDetailsLink(self, matchId):
        return self.getHeadLink() + DETAILS_KEY + matchId + API_KEY

    def getNameLink(self, ppid):
        return self.getHeadLink() + NAME_KEY + ppid + API_KEY

    def getPUUID(self, name, tag):
        return self.getHeadLink() + PUUID_KEY + name + '/' + tag + API_KEY
    




