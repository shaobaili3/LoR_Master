import constant as cs
import requests
import match

import re
import json
import webbrowser

class LocalInfo:    
    
    def __init__(self):
        self.opponentName = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False

    def updateStatus(self, checkOpponent):
        localLink = cs.geLocalLink(cs.PORT_NUM)
        try:
            localRequest = requests.get(localLink)
            self.isClientRuning = True
        except requests.exceptions.RequestException as e:
            isClientRuning = False
            return          
        details = localRequest.json()
        
        gameState = details['GameState']
        if gameState == 'InProgress':
            isInProgress = True
            name = details['OpponentName']
            if name != None:
                if name != self.opponentName:
                    self.opponentName = name
                    self.getTagByName(self.opponentName)

                    print(self.opponentName, self.opponentTag)
                    checkOpponent(self.opponentName, self.opponentTag)
        else:
            isInProgress = False

    def getTagByName(self, name):
        with open(cs.PLAYER_NA_PATH, encoding="utf8") as search:
            for line in search:
                fullName = line.rstrip().split('#')
                if name == fullName[0]:
                    # print(fullName)
                    self.opponentTag = fullName[1]
                    return
        print("Cannot find Opponent Tag")
        return


    #def statusListener(checkOpponent()):





# def getOpponentName():
#     localLink = cs.geLocalLink(cs.PORT_NUM)
#     try:
#         localRequest = requests.get(localLink)



#     except requests.exceptions.RequestException as e:
#         # print("Connection Error:", e)
#         print("游戏未启动")
#         return "Missing Client 3"  
#     details = localRequest.json()
#     #print(details)
#     return details['OpponentName']



    


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

            if len(deckCodes) >= 5:
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


    # def load():
    #     playerName = getOpponentName()
    #     if playerName == 'Missing Client 3':
    #         return
    #     elif playerName != None:
    #         playerTag = getTagByName(playerName)
    #         if playerTag != None:
    #             checkOpponent(playerName, playerTag)
    #         else:
    #             print("Cannot find player tag 数据库找不到用户名字")
    #     else :
    #         print("Rank game is not start yet, please start the game after matching. 比赛尚未开始, 匹配到对手后点击开始查询.")


    # def start():
    #     while True:
    #         a = input('Press Enter to start search opponent decks 按Enter回车开始对手套牌查询： ')
    #         load()
    #     return start



def start():
    local = LocalInfo()
    check = opponent()
    while True:
        local.updateStatus(check.checkOpponent)


start()

