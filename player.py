import webbrowser
import utility
import constants as cs
from leaderboard import getRankStr


class Player:
    def __init__(self, riot):
        self.sortedDecksCode = []
        self.riot = riot

    def checkOpponent(self, name, tag, showMessage, showMatchs, showDecks):
        puuid = self.riot.getPlayerPUUID(name, tag)
        if puuid is None:
            print("无法获取对手puuid")
            return
        matchIds = self.riot.getMatchs(puuid)
        if matchIds is None:
            print("无法获取对手最近对战记录")
            return
        else:
            if len(matchIds) > cs.MAX_NUM_DETAILS:
                matchIds = matchIds[0:cs.MAX_NUM_DETAILS]
        deckCodes = []
        loop = self.riot.asyncio.new_event_loop()
        self.riot.asyncio.set_event_loop(loop)
        tasks = [self.riot.aioMatchDetail(id) for id in matchIds]
        details = loop.run_until_complete(self.riot.asyncio.gather(*tasks))
        for detail in details:
            if str(detail).isdigit():
                print('Retry after ' + str(detail) + ', Riot server is busy.')
                showMessage('Riot server is busy, will restore in ' + str(detail) + ' seconds.')
                return
            if detail is None:
                continue
            else:
                if detail['info']['game_type'] != 'Ranked':
                    print(detail['info']['game_type'])
                    continue
            riotId = detail['metadata']['participants']
            for count, riotId in enumerate(riotId):
                if riotId == puuid:
                    myDetails = detail['info']['players'][count]
                    deckCodes.append(myDetails['deck_code'])
                    startTime = detail['info']['game_start_time_utc']
                    outcome = myDetails["game_outcome"]
                    showMatchs(utility.toLocalTimeString(startTime, True),
                               utility.getFactionString(myDetails["factions"]),
                               myDetails['deck_code'], outcome)
        print(self.getNoDuplicate(deckCodes))
        showDecks(self.getNoDuplicate(deckCodes), len(deckCodes))
        self.showOpponentAgain()

    def getNoDuplicate(self, deckCodes):
        deckslist = dict(
            zip(list(deckCodes),
                [list(deckCodes).count(i) for i in list(deckCodes)]))
        deckslist = dict(
            sorted(deckslist.items(), key=lambda item: item[1], reverse=True))
        # to-do
        self.sortedDecksCode = sorted(deckslist,
                                      key=deckslist.get,
                                      reverse=True)
        return deckslist

    def showOpponentAgain(self):
        if not self.riot.network.setting.autoOpenDeck:
            return
        if not self.sortedDecksCode:
            print("对手最近没有Rank记录")
            return
        print("已找到卡组:")
        for index, code in enumerate(self.sortedDecksCode):
            print('卡组', index + 1, '代码:', code)
        print("正在启动浏览器...(如果等待过长，请手动重启默认浏览器后，点击重新显示套牌按钮)")
        for index, code in enumerate(self.sortedDecksCode):
            webbrowser.open('https://lor.mobalytics.gg/decks/code/' + code)
            if index == 0:
                pass
            if index == 2:
                break
        print("卡组已在默认浏览器中显示, 请在浏览器中查看")

    def inspectPlayer(self, name, tag, showlog, showSummary, finishTrigger):
        puuid = self.riot.getPlayerPUUID(name, tag)
        if puuid is None:
            print('查询失败, puuid为空')
            return finishTrigger('Couldn\'t find player ' + name + '#' + tag)
        matchIds = self.riot.getMatchs(puuid)
        winNum = 0
        matchNum = 0
        if matchIds is None:
            print('查询失败, matchid为空')
            return finishTrigger(name + '#' + tag +
                                 ' has no recent match records')
        deckCodes = []
        for matchId in matchIds:
            if matchNum == cs.MAX_NUM_DETAILS:
                break
            detail = self.riot.getDetail(matchId)
            # print('type:', str(type(detail)))
            if str(detail).isdigit():
                print('Retry after ' + str(detail) + ', Riot server is busy.')
                finishTrigger('Riot server is busy, will restore in ' + str(detail) + ' seconds.')
                return
            if detail is None:
                continue
            print('detail', detail)
            startTime = detail['info']['game_start_time_utc']
            if detail['info']['game_type'] != 'Ranked':
                print(detail['info']['game_type'], detail['info']['game_mode'],
                      utility.toLocalTimeString(startTime))
                continue
            else:
                matchNum += 1
            riotId = detail['metadata']['participants']
            outcome = None
            opponentDetail = None
            myDetails = None
            totalTurn = detail['info']['total_turn_count']
            opName = ['', '']
            fullName = ''
            for count, riotId in enumerate(riotId):
                # to check if this is opponent record
                if riotId != puuid:
                    opName = self.riot.getPlayerName(riotId)
                    fullName = opName[0] + '#' + opName[1]
                    print(
                        str(matchNum) + ". " + fullName + ' ' +
                        utility.toLocalTimeString(startTime))
                    opponentDetail = detail['info']['players'][count]
                else:
                    myDetails = detail['info']['players'][count]
                    outcome = myDetails["game_outcome"]
                    if outcome == 'win':
                        winNum += 1
            # opName = self.riot.getPlayerName(opponentDetail['puuid'])[0]
            rank = ''
            print(outcome + "   " + str(myDetails["factions"]) +
                  myDetails['deck_code'] + str(opponentDetail["factions"]) +
                  " " + opponentDetail['deck_code'])
            deckCodes.append(myDetails['deck_code'])
            settingServer = self.riot.network.setting.getServer()
            rank = getRankStr(opName[0], settingServer)
            showlog(fullName + ' ' + rank,
                    utility.toLocalTimeString(startTime), outcome,
                    myDetails['deck_code'],
                    utility.getFactionString(myDetails["factions"]),
                    opponentDetail['deck_code'],
                    utility.getFactionString(opponentDetail["factions"]),
                    totalTurn, matchNum)
        if matchNum != 0:
            print(
                str(winNum) + ' wins' + ' out of ' + str(matchNum) +
                ' rank matchs')
            print("Win rate: " + str(int(winNum / matchNum * 100)) + "%")
            showSummary(self.getNoDuplicate(deckCodes))
            return finishTrigger(name + '#' + tag, ' win rate: ' +
                                 str(int(winNum / matchNum * 100)) + "%  " +
                                 str(winNum) + ' wins' + ' out of ' +
                                 str(matchNum) + ' rank matchs')
        else:
            print('无法获取对战历史数据')
            return finishTrigger(name + '#' + tag,
                                 ' has no recent rank match records')
