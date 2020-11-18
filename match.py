import constant
import requests
import constant as cs

import aiohttp
import asyncio

class Match():
    def __init__(self) -> None:
        return

    def getMatchDetails(self, matchId):
        return

    def getPlayerPUUID(self, name, tag):
        puuidLink = cs.getPUUID(name, tag)
        try:
            puuidRequest =requests.get(puuidLink)
        except requests.exceptions.RequestException as e:
            print(puuidLink)
            print(e)
            print('无法连接PUUID服务器')
            return None
        idDetails = puuidRequest.json()
        if idDetails is dict:
            status = idDetails.get('status')
            if status is not None:
                print('PUUID服务器错误: ', status)
                return None
        return idDetails.get('puuid')

    def getMatchs(self, ppid):
        matchLink = cs.getMatchsLink(ppid)
        try:
            matchRequest =requests.get(matchLink)
        except requests.exceptions.RequestException as e:
            print(matchLink)
            print(e)
            print('无法连接比赛ID服务器')
            return None
        matchIds = matchRequest.json()

        if matchIds is dict:
            status = matchIds.get('status')
            if status is not None:
                print('比赛ID服务器错误: ', status)
                return None
        return matchIds

    def getDetails(self, matchId):
        detailsLink = cs.getDetailsLink(matchId)
        try:
            detailsRequest = requests.get(detailsLink)
        except requests.exceptions.RequestException as e:
            print(detailsLink)
            print(e)
            print('无法连接比赛内容服务器')
            return None
        details = detailsRequest.json()
        if details is dict:
            status = details.get('status')
            if status is not None:
                print('比赛内容服务器错误: ', status)
                return None
        return details


    def getPlayerName(self, ppid):
        nameLink = cs.getNameLink(ppid)
        try:
            nameRequest =requests.get(nameLink)
        except requests.exceptions.RequestException as e:
            print(nameLink)
            print(e)
            print('无法连接用户名字 by PPID服务器')
            return '名字Unknow'
        name = nameRequest.json()
        if name is dict:
            status = name.get('status')
            if status is not None:
                print('用户名字 by PPID服务器错误: ', status)
                return '名字Unknow'
        return name['gameName'] + "#" + name['tagLine']



