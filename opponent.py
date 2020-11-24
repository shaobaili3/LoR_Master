from local import Local
from match import Match
import json
import webbrowser
#from win10toast import ToastNotifier
#import asyncio
from PIL import Image

match = Match()

class Opponent:
    def __init__(self):
        self.sortedDecksCode = None
        #self.toaster = ToastNotifier()

    def checkOpponent(self, name, tag):
        puuid = match.getPlayerPUUID(name, tag)
        matchIds = match.getMatchs(puuid)
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
        sortedDecksCode = sorted(Deckslist, key = Deckslist.get, reverse=True)
        self.sortedDecksCode = sortedDecksCode
        for index, code in enumerate(sortedDecksCode):
            webbrowser.open('https://www.yaytears.com/runeterra/deck/' + code)
            if index == 0:
                # self.toaster.show_toast("Opponent Deck Found", name + "#" +  tag, icon_path="icon.ico", duration=3)
                break
            if index == 2:
                break

    def showOpponentAgain(self):
        if self.sortedDecksCode is None:
            return
            #self.toaster.show_toast("LOR大师", "历史记录不可用", icon_path="icon.ico", duration=1)

        for index, code in enumerate(self.sortedDecksCode):
            webbrowser.open('https://www.yaytears.com/runeterra/deck/' + code)
            if index == 0:
                pass
                #notification.notify(title="", message="", app_name='LOL MASTER', app_icon="icon.ico", timeout=8, ticker='', toast = False)
                #self.toaster.show_toast("LOR大师", "已找到历史记录", icon_path="icon.ico", duration=1)
            if index == 2:
                break