import requests
import Models.network

LEADERBOARD_HEROKU = 'https://lmtservice.herokuapp.com/leaderboard/'


class Heroku():
    def __init__(self) -> None:
        self.session = requests.Session()

    def getMatches(self, server):
        leaderboardLink = LEADERBOARD_HEROKU + server
        try:
            leaderboardRequest = self.session.get(
                leaderboardLink, proxies=Models.network.getProxy())
        except requests.exceptions.RequestException as e:
            print('getMatches error: ', e)
            return None
        
        if leaderboardRequest.ok:
            return leaderboardRequest.json()
        
        print(leaderboardRequest.headers)
        print(leaderboardRequest.status_code)
        return None
