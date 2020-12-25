import json
import webbrowser

class Opponent:
    def __init__(self, match):
        self.sortedDecksCode = []
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
        else:
            #print(len(matchIds))
            if len(matchIds) > 8:
                matchIds = matchIds[0:8]
                #print(len(matchIds))
        deckCodes = []
        loop = self.match.asyncio.new_event_loop()
        self.match.asyncio.set_event_loop(loop)
        tasks = [self.match.aioGetDetail(id) for id in matchIds]
        details = loop.run_until_complete(self.match.asyncio.gather(*tasks))
        for detail in details:
            if detail is None:
                continue
            else:
                if detail['info']['game_type'] != 'Ranked':
                    print(detail['info']['game_type'])
                    continue
            ppids = detail['metadata']['participants']
            for count, ppid in enumerate(ppids):
                if ppid == puuid:
                    myDetials = detail['info']['players'][count]
                    deckCodes.append(myDetials['deck_code'])
                    # print(str(myDetials["factions"]) + myDetials['deck_code'])
        Deckslist = dict(zip(list(deckCodes),[list(deckCodes).count(i) for i in list(deckCodes)]))
        self.sortedDecksCode = sorted(Deckslist, key = Deckslist.get, reverse=True)
        self.showOpponentAgain()

    # def checkOpponent(self, name, tag):
    #     puuid = self.match.getPlayerPUUID(name, tag)
    #     if puuid is None:
    #         print("无法获取对手puuid")
    #         return
    #     matchIds = self.match.getMatchs(puuid)
    #     if matchIds is None:
    #         print("无法获取对手最近对战记录")
    #         return
    #     deckCodes = []
    #     for matchid in matchIds:
    #         details = self.match.getDetails(matchid)
    #         if details is None:
    #             continue
    #         else:
    #             if details['info']['game_type'] != 'Ranked':
    #                 print(details['info']['game_type'])
    #                 continue
    #         ppids = details['metadata']['participants']
    #         if len(deckCodes) == 10:
    #             break
    #         for count, ppid in enumerate(ppids):
    #             if ppid == puuid:
    #                 myDetials = details['info']['players'][count]
    #                 deckCodes.append(myDetials['deck_code'])
    #                 print(str(myDetials["factions"]) + myDetials['deck_code'])
    #     Deckslist = dict(zip(list(deckCodes),[list(deckCodes).count(i) for i in list(deckCodes)]))
    #     self.sortedDecksCode = sorted(Deckslist, key = Deckslist.get, reverse=True)
    #     self.showOpponentAgain()        

    def showOpponentAgain(self):
        if not self.sortedDecksCode:
            print("对手最近没有Rank记录")
            return
        print("已找到卡组:")
        for index, code in enumerate(self.sortedDecksCode):
            print('卡组', index + 1, '代码:' ,code)
        print("正在启动浏览器...(如果等待过长，请手动重启默认浏览器后，点击重新显示套牌按钮)")
        for index, code in enumerate(self.sortedDecksCode):
            webbrowser.open('https://www.yaytears.com/runeterra/deck/' + code)
            if index == 0:
                pass
            if index == 2:
                break
        print("卡组查询已完成")