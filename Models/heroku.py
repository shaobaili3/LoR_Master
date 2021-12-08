import requests
import Models.network

LEADERBOARD_HEROKU = 'https://lmtservice.herokuapp.com/leaderboard/'
HISTORY_HEROKU = 'https://lormaster.herokuapp.com/history/'
SEARCH_HEROKU = 'https://lormaster.herokuapp.com/search/'
TAG_HEROKU = 'https://lormaster.herokuapp.com/tag/'


class Heroku():
    def __init__(self, leaderboard) -> None:
        self.leaderboard = leaderboard
        self.session = requests.Session()

    def getTag(self, server, name):
        tagLink = TAG_HEROKU + server + '/' + name
        try:
            tagRequest = self.session.get(
                tagLink, proxies=Models.network.getProxy())
        except requests.exceptions.RequestException as e:
            print('getMatches error: ', e)
            return None
        if tagRequest.ok:
            return tagRequest.json()

        print(tagRequest.headers)
        print(tagRequest.status_code)
        return None

    def getHistory(self, server, name, id):
        leaderboardLink = HISTORY_HEROKU + server + '/' + name + '/' + id
        try:
            historyRequest = self.session.get(
                leaderboardLink, proxies=Models.network.getProxy())
        except requests.exceptions.RequestException as e:
            print('getMatches error: ', e)
            return None

        if historyRequest.ok:
            return historyRequest.json()

        print(historyRequest.headers)
        print(historyRequest.status_code)
        return None

    def getSearch(self, server, name, id):
        detailLink = SEARCH_HEROKU + server + '/' + name + '/' + id
        try:
            detailRequest = self.session.get(
                detailLink, proxies=Models.network.getProxy())
        except requests.exceptions.RequestException as e:
            print('getMatches error: ', e)
            return None

        if detailRequest.ok:
            details = detailRequest.json()
            for detail in details:
                self.addPlayerInfo(detail, server)
            return details

        print(detailRequest.headers)
        print(detailRequest.status_code)
        return None

    def addPlayerInfo(self, detail, server):
        try:
            playerNames = detail['playernames']
        except Exception as e:
            print('processMatchDetail error', e)
            return detail
        playernames = []
        player_info = []
        for name in playerNames:
            fullName = name.split('#', 1)
            name, tag = fullName[0], fullName[1]
            rank, lp = self.leaderboard.checkRank(name, server)
            playernames.append(name + '#' + tag)
            player_info.append(
                {'name': name, 'tag': tag, 'rank': rank, 'lp': lp})
        detail['player_info'] = player_info
