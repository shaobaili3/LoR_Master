import constant
import requests
import match
import re
from constant import geLocalLink
import json
import webbrowser

from match import getPlayerPUUID


def getOpponentName():
    localLink = geLocalLink('21337')
    localRequest = requests.get(localLink)
    details = localRequest.json()
    #print(details)
    return details['OpponentName']


def getTagByName(name):
    if name == None:
        #print("Name is None")
        return

    tag = None
    with open("playerNames.txt", encoding="utf8") as search:
        for line in search:
            fullName = line.rstrip().split('#')
            if name == fullName[0]:
               # print(fullName)
                tag = fullName[1]
    return tag
    

def checkOpponent(name, tag):
    puuid = getPlayerPUUID(name, tag)
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
        if countNum >= 1:
            break
        countNum += 1


def load():
    playerName = getOpponentName()
    if playerName != None:
        playerTag = getTagByName(playerName)
        if playerTag != None:
            checkOpponent(playerName, playerTag)
        else:
            print("Cannot find player tag 数据库找不到用户名字")
    else:
        print("Opponent name is None 比赛尚未开始, 匹配到对手后点击开始查询")


def start():
    while True:
        a = input('Press enter to start search opponent decks 按Enter开始对手套牌查询： ')
        load()

start()
