import Models.utility as utility
import constants as cs
from uiModels import DeckDetail
import Models.network
from uiModels import OpponentFlask


class Player:
    def __init__(self, riot, leaderboard):
        self.sortedDecksCode = []
        self.riot = riot
        self.summary = {}
        self.historyFlask = OpponentFlask()
        self.matchesJson = []
        self.leaderboard = leaderboard

    def addMatchToSummary(self, code, outcome, time):
        if code in self.summary:
            self.summary[code].matches += 1
            if outcome == 'win':
                self.summary[code].winNum += 1
        else:
            winNum = 0
            if outcome == 'win':
                winNum = 1
            self.summary[code] = DeckDetail(1, winNum, time)

        for key in self.summary:
            if key != code:
                self.summary[key].history += 'E'
            else:
                if outcome == 'win':
                    self.summary[key].history += 'W'
                else:
                    self.summary[key].history += 'L'

        matchNum = len(self.summary[list(self.summary.keys())[0]].history)

        for key in self.summary:
            fill = 'E' * (matchNum - len(self.summary[key].history))
            self.summary[key].history = fill + self.summary[key].history

    def loadMatchsToFlask(self):
        self.historyFlask.history = []
        for deckCode in self.summary:
            match = {}
            match['time'] = self.summary[deckCode].time
            match['deckCode'] = deckCode
            match['matches'] = self.summary[deckCode].matches
            match['winrate'] = self.summary[
                deckCode].winNum / self.summary[deckCode].matches
            match['history'] = self.summary[deckCode].history
            self.historyFlask.history.append(match)

    def inspectFlask(self, name, tag, maxNum=cs.MAX_NUM_DETAILS):
        self.matchesJson = []
        puuid = self.riot.getPlayerPUUID(name, tag)
        if puuid is None:
            print(
                '', name + '#' + tag + ' does not exist. Please check player name and player tag')
            return
        matchIds = self.riot.getMatches(puuid)
        if matchIds is None:
            print(name + '#' + tag,
                  ' has no recent match records')
            return
        matchNum, winNum = self.processMatchIds(
            matchIds, puuid, name, tag, maxNum)

        if matchNum != 0:
            print(
                str(winNum) + ' wins' + ' out of ' + str(matchNum) +
                ' rank matchs')
            print("Win rate:", str(int(winNum / matchNum * 100)) + "%")
            return
        else:
            print(name + '#' + tag,
                  ' has no recent rank match records')
            return

    def processMatchIds(self, matchIds, puuid, name, tag, maxNum):
        self.summary = {}
        deckCodes = []
        winNum = 0
        matchNum = 0
        for matchId in matchIds:
            try:
                # If match number bigger than MAX, getDetail will only ruturn data from cache
                detail = self.riot.getDetail(matchId, matchNum, maxNum)
                if str(detail).isdigit():
                    print(
                        'Riot server [' + Models.network.API_KEY[-4:] + '] busy ' + str(detail))
                    continue
                if detail is None:
                    continue
                print('detail', detail)
                gameMode = detail['info']['game_mode']
                gameType = detail['info']['game_type']
                startTime = detail['info']['game_start_time_utc']

                if gameMode in cs.UNSUPPORTED_MODE:
                    continue

                if gameType in cs.UNSUPPORTED_TYPE:
                    continue

                self.matchesJson.append(
                    self.addPlayerInfoToMatchDetail(detail))
                matchNum += 1
                riotId = detail['metadata']['participants']
                outcome = None
                opponentDetail = None
                myDetails = None
                totalTurn = detail['info']['total_turn_count']
                myIndex = 1
                opponentIndex = 0
                if riotId[0] == puuid:
                    myIndex = 0
                    opponentIndex = 1
                else:
                    # differnet APIs has df puuid, has to double check if equal playernames when may using caching data
                    indexName = self.riot.getPlayerName(riotId[0])
                    if indexName[0].lower() == name.lower() and indexName[1].lower() == tag.lower():
                        myIndex = 0
                        opponentIndex = 1
                opName = self.riot.getPlayerName(riotId[opponentIndex])
                fullName = opName[0] + '#' + opName[1]
                opponentDetail = detail['info']['players'][opponentIndex]
                myDetails = detail['info']['players'][myIndex]
                outcome = myDetails["game_outcome"]
                if outcome == 'win':
                    winNum += 1
                self.addMatchToSummary(
                    myDetails['deck_code'], outcome, utility.toLocalTimeString(startTime, True))
                deckCodes.append(myDetails['deck_code'])
                settingServer = self.riot.network.setting.riotServer
                rank = 0
                gameTypeString = '[' + gameType + ']'
                if gameType == '':
                    gameTypeString = ''
                print(fullName + ' ' + rank,
                      gameTypeString + ' [' + gameMode + '] ' +
                      utility.toLocalTimeString(startTime), outcome,
                      myDetails['deck_code'],
                      utility.getFactionString(myDetails["factions"]),
                      opponentDetail['deck_code'],
                      utility.getFactionString(opponentDetail["factions"]),
                      str(totalTurn) + ' Order of Play: ' + str(myDetails['order_of_play']), matchNum)
            except Exception as e:
                print('Read MatchId Error match id: ', matchId, e)
                continue
        return matchNum, winNum

    def addPlayerInfoToMatchDetail(self, detail):
        try:
            playerPuuids = detail['metadata']['participants']
        except Exception as e:
            print('processMatchDetail error', e)
            return detail
        playernames = []
        player_info = []
        for puuid in playerPuuids:
            name, tag = self.riot.getPlayerName(puuid)
            rank, lp = self.leaderboard.checkRank(
                name, self.riot.network.setting.riotServer)
            playernames.append(name + '#' + tag)
            player_info.append(
                {'name': name, 'tag': tag, 'rank': rank, 'lp': lp})
        detail['playernames'] = playernames
        detail['player_info'] = player_info
        return detail
