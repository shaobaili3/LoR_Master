from local import Local
from match import Match
import json
import webbrowser

match = Match()

class opponent:
    def checkOpponent(self, name, tag):
        puuid = match.getPlayerPUUID(name, tag)
        matchIds = match.getMatchs(puuid)
        deckCodes = []
        for matchid in matchIds:
            details = match.getDetails(matchid)
            if details['info']['game_type'] != 'Ranked':
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
        sortedDecksCode = sorted(Deckslist, key = Deckslist.get, reverse=True)
        countNum = 0
        for code in sortedDecksCode:
            webbrowser.open('https://www.yaytears.com/runeterra/deck/' + code)
            if countNum >= 2:
                break
            countNum += 1


def start():
    local = Local()
    check = opponent()
    while True:
        local.updateStatus(check.checkOpponent)


start()
