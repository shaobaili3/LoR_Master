from local import Local
from match import Match
import json
import webbrowser
from PIL import Image

match = Match()

class Opponent:
    def __init__(self):
        self.sortedDecksCode = None

    def checkOpponent(self, name, tag):
        puuid = match.getPlayerPUUID(name, tag)
        if puuid is None:
            print("无法获取对手puuid")
            return

        matchIds = match.getMatchs(puuid)
        if matchIds is None:
            print("无法获取对手最近对战ids")
            return

        deckCodes = []
        
        for matchid in matchIds:
            details = match.getDetails(matchid)
            if details is None:
                continue
            else:
                if details['info']['game_type'] != 'Ranked':
                    print(details['info']['game_type'])
                    continue
            ppids = details['metadata']['participants']
            myDetials = None

            if len(deckCodes) == 5:
                break

            for count, ppid in enumerate(ppids):
                if ppid == puuid:
                    myDetials = details['info']['players'][count]
                    deckCodes.append(myDetials['deck_code'])
                    print(str(myDetials["factions"]) + myDetials['deck_code'])
        Deckslist = dict(zip(list(deckCodes),[list(deckCodes).count(i) for i in list(deckCodes)]))
        self.sortedDecksCode = sorted(Deckslist, key = Deckslist.get, reverse=True)
        self.showOpponentAgain()

    def showOpponentAgain(self):
        print("open2")
        if self.sortedDecksCode is None:
            print("没有相关套牌")
            return

        for index, code in enumerate(self.sortedDecksCode):
            print(code)
            webbrowser.open('https://www.yaytears.com/runeterra/deck/' + code)
            if index == 0:
                pass
            if index == 2:
                break