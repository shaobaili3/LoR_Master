API_KEY2 = '?api_key=' + 'RGAPI-3dd1641a-6d80-458d-9fb5-357253d7674b'  #product
API_KEY = '?api_key=' + 'RGAPI-3b5bde16-66b4-4943-b8fa-241d27b29344'  #personal
MATCH_KEY = '.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = '.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PUUID_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'



class Network():
    def __init__(self, setting) -> None:
        self.setting = setting
        self.key = API_KEY
        return

    def getHeadLink(self):
        return 'https://' + self.setting.getServer()

    def getMatchsLink(self, ppid):
        return self.getHeadLink() + MATCH_KEY + ppid + '/ids' + self.key

    def getDetailsLink(self, matchId):
        return self.getHeadLink() + DETAILS_KEY + matchId + self.key

    def getNameLink(self, ppid):
        return self.getHeadLink() + NAME_KEY + ppid + self.key

    def getPUUID(self, name, tag):
        return self.getHeadLink() + PUUID_KEY + name + '/' + tag + self.key

    def switchAPIKey(self):
        if self.key == API_KEY:
            self.key = API_KEY2
        else:
            self.key = API_KEY
