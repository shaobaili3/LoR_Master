import constants as cs
from uiModels import DeckSummary
import Models.heroku
import threading
import time

class Player:
    def __init__(self, riot, leaderboard):
        self.sortedDecksCode = []
        self.riot = riot
        self.summaries = {}
        self.matchesJson = []
        self.leaderboard = leaderboard
        self.error = {
            "status": {
                "message": "error",
                "error": 0,
                "code": 404
            }
        }

    def setError(self, message, error, code=404):
        self.error = {}
        self.error['status'] = {}
        self.error['status']['message'] = message
        self.error['status']['error'] = error
        self.error['status']['code'] = code
        print('error', self.error)

    def addMatchToSummary(self, code, outcome, startTime):
        if code in self.summaries:
            self.summaries[code].matches += 1
            if outcome == 'win':
                self.summaries[code].winNum += 1
        else:
            winNum = 0
            if outcome == 'win':
                winNum = 1
            self.summaries[code] = DeckSummary(1, winNum, startTime, code)

        for key in self.summaries:
            if key != code:
                self.summaries[key].history += 'E'
            else:
                if outcome == 'win':
                    self.summaries[key].history += 'W'
                else:
                    self.summaries[key].history += 'L'

        matchNum = len(self.summaries[list(self.summaries.keys())[0]].history)

        for key in self.summaries:
            fill = 'E' * (matchNum - len(self.summaries[key].history))
            self.summaries[key].history = fill + self.summaries[key].history

    def inspectFlask(self, name, tag, matchIds):
        self.error = None
        self.matchesJson = []
        self.summaries = {}
        # puuid = self.riot.getPlayerPUUID(name, tag)
        # if puuid is None:
        #     errorMessage = str(
        #         '' + name + '#' + tag + ' does not exist. Please check player name and player tag')
        #     self.setError(errorMessage, 0)
        #     return
        if matchIds is None:
            errorMessage = str(name + '#' + tag +
                               ' has no recent match records')
            self.setError(errorMessage, 1)
            return
        matchNum = self.processMatchIds(
            matchIds, name, tag)

        if matchNum == 0:
            errorMessage = str(name + '#' + tag +
                               ' has no recent rank match records')
            self.setError(errorMessage, 2)
            return

    def processMatchIds(self, matchIds, name, tag):
        deckCodes = []
        matchNum = 0
        for matchId in matchIds:
            #try:
                # If match number bigger than MAX, getDetail will only ruturn data from cache
                id = name + '#' + tag
                detail = self.riot.getDetail(matchId, matchNum, 20, id)
                if detail is None:
                    continue
                gameMode = detail['info']['game_mode']
                gameType = detail['info']['game_type']
                # startTime = detail['info']['game_start_time_utc']

                print(matchId, gameMode, gameType)

                if gameMode in cs.UNSUPPORTED_MODE:
                    continue

                if gameMode not in cs.SUPPORTED_MODE:
                    continue

                if gameType in cs.UNSUPPORTED_TYPE:
                    continue
                
                if detail.get('playernames') is None:
                    return

                self.addPlayerInfo(detail)
                self.matchesJson.append(detail)
                matchNum += 1
                # riotId = detail['metadata']['participants']
                # outcome = None
                # myDetails = None
                # myIndex = 1
                # if riotId[0] == puuid:
                #     myIndex = 0
                # else:
                #     # differnet APIs has df puuid, has to double check if equal playernames when may using caching data
                #     indexName = self.riot.getPlayerName(riotId[0])
                #     if indexName[0].lower() == name.lower() and indexName[1].lower() == tag.lower():
                #         myIndex = 0
                # myDetails = detail['info']['players'][myIndex]
                # outcome = myDetails["game_outcome"]
                # self.addMatchToSummary(
                #     myDetails['deck_code'], outcome, startTime)
                # deckCodes.append(myDetails['deck_code'])
            # except Exception as e:
            #     print('Read MatchId Error match id: ', matchId, e)
            #     continue
        return matchNum

    def addPlayerInfo(self, detail):
        if detail.get('player_info') is not None:
            return
        try:
            playerPuuids = detail['playernames']
        except Exception as e:
            print('processMatchDetail error', e)
            return detail
        playernames = []
        player_info = []
        for name in playernames:
            fullName = name.split('#', 1)
            name, tag = fullName[0], fullName[1]
            rank, lp = self.leaderboard.checkRank(
                name, self.riot.network.setting.riotServer)
            playernames.append(name + '#' + tag)
            player_info.append(
                {'name': name, 'tag': tag, 'rank': rank, 'lp': lp})
        detail['playernames'] = playernames
        detail['player_info'] = player_info
