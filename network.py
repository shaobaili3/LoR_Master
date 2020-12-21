API_KEY = '?api_key=' + 'RGAPI-3dd1641a-6d80-458d-9fb5-357253d7674b'

MATCH_KEY = '.api.riotgames.com/lor/match/v1/matches/by-puuid/'
DETAILS_KEY = '.api.riotgames.com/lor/match/v1/matches/'
NAME_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
PUUID_KEY = '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'

LOCAL_KEY = '/positional-rectangles'
IP_KEY = 'http://127.0.0.1:'

PORT_NUM = '21337'

PLAYER_NA_PATH = 'Resource/NA.dat'


def geLocalLink(port):
        return IP_KEY + port + LOCAL_KEY

class Network():
    def __init__(self, serverName = 'americas') -> None:
        self.serverName = serverName
        self.headLink = 'https://' + serverName
        return

    def getMatchsLink(self, ppid):
        return self.headLink + MATCH_KEY  + ppid + '/ids' + API_KEY

    def getDetailsLink(self, matchId):
        return self.headLink + DETAILS_KEY + matchId + API_KEY

    def getNameLink(self, ppid):
        return self.headLink + NAME_KEY + ppid + API_KEY

    def getPUUID(self, name, tag):
        return self.headLink + PUUID_KEY + name + '/' + tag + API_KEY

