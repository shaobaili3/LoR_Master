import json
import webbrowser

class Opponent:
    def __init__(self, match):
        self.sortedDecksCode = None
        self.match = match

    def checkOpponent(self, name, tag):
        puuid = self.match.getPlayerPUUID(name, tag)
        if puuid is None:
            print("无法获取对手puuid")
            return

        matchIds = self.match.getMatchs(puuid)
        if matchIds is None:
            print("无法获取对手最近对战记录")
            return

        deckCodes = []
        
        for matchid in matchIds:
            details = self.match.getDetails(matchid)
            if details is None:
                continue
            else:
                if details['info']['game_type'] != 'Ranked':
                    print(details['info']['game_type'])
                    continue
            ppids = details['metadata']['participants']
            if len(deckCodes) == 10:
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
        
        if self.sortedDecksCode is None:
            print("没有相关套牌")
            return

        print("正在启动浏览器...(如果等待过长，请手动重启默认浏览器后，点击重新显示套牌按钮)")

        for index, code in enumerate(self.sortedDecksCode):
            print('套牌', index + 1, '代码:' ,code)
            webbrowser.open('https://www.yaytears.com/runeterra/deck/' + code)
            if index == 0:
                pass
            if index == 2:
                break