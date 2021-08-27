from Models.network import Network
import Models.network
import requests
import aiohttp
import asyncio
import json
import os
import constants

class Riot:
    def __init__(self, network):
        self.network = network
        self.asyncio = asyncio
        self.loop = None
        self.matchDetails = {}
        self.riotIds = {}
        self.playerNames = {}
        self.matches = {}
        self.loadJson()
        self.session = requests.Session()
        return

    def loadJson(self):
        try:
            with open('data/matchDetails.json', 'r', encoding='utf-8') as fp:
                self.matchDetails = json.load(fp)
            with open('data/riotIds.json', 'r', encoding='utf-8') as fp:
                self.riotIds = json.load(fp)
            with open('data/playerNames.json', 'r', encoding='utf-8') as fp:
                self.playerNames = json.load(fp)
            with open('data/matches.json', 'r', encoding='utf-8') as fp:
                self.matches = json.load(fp)
        except Exception as e:
            print('loadJson error', e)
            return

    def save(self):
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/matchDetails.json', 'w+', encoding='utf-8') as fp:
                json.dump(self.matchDetails, fp, ensure_ascii=False, indent= 2)
            with open('data/riotIds.json', 'w+', encoding='utf-8') as fp:
                json.dump(self.riotIds, fp, ensure_ascii=False, indent= 2)
            with open('data/playerNames.json', 'w+', encoding='utf-8') as fp:
                json.dump(self.playerNames, fp, ensure_ascii=False, indent= 2)
        except Exception as e:
            print('save cache error: ', e)
            return

    # Should not use cache, because you cannot identify capital letters of playernames
    def getPlayerPUUID(self, name, tag):

        # Developer keys expose in cache. 'lower()' make sure link will not change by case sensitivity.
        puuidLink = self.network.getPUUID(name.lower(), tag.lower())

        masterId = puuidLink

        if masterId in self.riotIds:
            return self.riotIds[masterId]
        print(puuidLink)
        try:
            puuidRequest = self.session.get(puuidLink)
        except requests.exceptions.RequestException as e:
            print(puuidLink)
            print(e)
            print('无法连接getPlayerPUUID服务器')
            return None
        idDetails = puuidRequest.json()
        header = puuidRequest.headers
        if not puuidRequest.ok:
            print(puuidLink)
            print(puuidRequest.headers)
            print(puuidRequest.status_code)
            print('userId -> PUUID服务器错误')
            print(idDetails)
            if 'Retry-After' in header:
                print('getPlayerPUUID服务器正忙', header['Retry-After'], '秒')
                Models.network.switchAPI()
            return None
        else:
            puuid = idDetails.get('puuid')
            gameName = idDetails.get('gameName')
            tagLine = idDetails.get('tagLine')
            if puuid is not None:
                self.riotIds[masterId] = puuid
                self.playerNames[puuid] = gameName, tagLine
                self.save()
            return puuid


    def saveMatchesInCache(self, puuid, matchIds):
        playName = self.getPlayerName(puuid)
        server = self.network.setting.riotServer
        uniqueName = playName[0] + playName[1] + server
        matchIdsCache = self.matches.get(uniqueName)
        if matchIdsCache is not None:
            new = matchIds + list(set(matchIdsCache) - set(matchIds))
            self.matches[uniqueName] = new
        else:
            self.matches[uniqueName] = matchIds
        os.makedirs('data', exist_ok=True)
        with open('data/matches.json', 'w+', encoding='utf-8') as fp:
            json.dump(self.matches, fp)

    def getMatchesInCache(self, puuid):
        playName = self.getPlayerName(puuid)
        server = self.network.setting.riotServer
        uniqueName = playName[0] + playName[1] + server
        return self.matches[uniqueName]


    def getMatches(self, puuid, saveCache = True):
        matchLink = self.network.getMatchesLink(puuid)
        try:
            matchRequest = self.session.get(matchLink)
        except requests.exceptions.RequestException as e:
            print(matchLink)
            print(e)
            print('无法连接比赛ID服务器')
            return None
        matchIds = matchRequest.json()
        header = matchRequest.headers
        if not matchRequest.ok:
            print(matchLink)
            print(matchRequest.headers)
            print(matchRequest.status_code)
            print('getmatches server error')
            print(matchIds)
            if 'Retry-After' in header:
                print('getmatches server busy', header['Retry-After'], '秒')
                Models.network.switchAPI()
            return None
        if saveCache:
            self.saveMatchesInCache(puuid, matchIds)
            return self.getMatchesInCache(puuid)
        return matchIds
        #   return matchIds

    async def aioMatchDetail(self, matchId):
        if matchId in self.matchDetails:
            return self.matchDetails[matchId]
        async with aiohttp.ClientSession() as session:
            try:
                detailsLink = self.network.getDetailsLink(matchId)
                async with session.get(detailsLink) as resp:
                    detail = await resp.json()
            except aiohttp.ClientConnectionError as e:
                print('aioMatchDetail Error: ', e)
                return None
        header = resp.headers
        if 'X-Method-Rate-Limit-Count' in header:
            print('X-Method-Rate-Limit-Count: ',
                  header['X-Method-Rate-Limit-Count'])
            print('X-App-Rate-Limit', header['X-App-Rate-Limit'])

        if 'Retry-After' in header:
            print('aio服务器正忙,请等待', header['Retry-After'], '秒')
            Models.network.switchAPI()
            return header['Retry-After']

        if resp.ok:
            self.matchDetails[matchId] = detail
            self.save()
            return detail
        else:
            print('AIO比赛内容服务器错误: ', resp.status)
            print(detailsLink)
            print(detail)
            return None
            
    def getDetail(self, matchId, matchIndex = 1):
        # If matchIndex bigger than MAX, only pull data from cache
        if matchIndex > constants.MAX_NUM_DETAILS - 1:
            return self.matchDetails.get(matchId)

        if matchId in self.matchDetails:
            return self.matchDetails[matchId]
        detailsLink = self.network.getDetailsLink(matchId)
        try:
            detailsRequest = self.session.get(detailsLink)
        except requests.exceptions.RequestException as e:
            print(detailsLink)
            print(e)
            print('无法连接比赛内容服务器')
            return None
        detail = detailsRequest.json()
        header = detailsRequest.headers
        if 'X-Method-Rate-Limit-Count' in header:
            print('X-Method-Rate-Limit-Count: ',
                  header['X-Method-Rate-Limit-Count'])
            print('X-App-Rate-Limit', header['X-App-Rate-Limit'])
        if not detailsRequest.ok:
            print(detailsLink)
            print(header)
            print(detailsRequest.status_code)
            print(detail)
            print('比赛内容服务器错误')
            if 'Retry-After' in header:
                print('服务器正忙,请等待', header['Retry-After'], '秒')
                Models.network.switchAPI()
                return header['Retry-After']
            return None
        else:
            self.matchDetails[matchId] = detail
            self.save()
        if detail is None:
            print('比赛内容服务返回空')
        return detail

    # 在main中使用和inspector中使用
    def getPlayerName(self, puuid):
        if puuid in self.playerNames:
            return self.playerNames[puuid]
        nameLink = self.network.getNameLink(puuid)
        try:
            nameRequest = self.session.get(nameLink)
        except requests.exceptions.RequestException as e:
            print(nameLink)
            print(e)
            print('无法连接puuid->userId服务器')
            return '名字Unknow', 'unknow'
        name = nameRequest.json()
        header = nameRequest.headers
        #headers = nameRequest.headers
        # print(headers)
        if not nameRequest.ok:
            print(nameLink)
            print(nameRequest.headers)
            print(nameRequest.status_code)
            print(name)
            print('puuid->userid服务器错误:')
            if 'Retry-After' in header:
                print('服务器正忙,请等待', header['Retry-After'], '秒')
                Models.network.switchAPI()
            return 'Unknow', str(puuid)[0:5]
        else:
            self.playerNames[puuid] = name['gameName'], name['tagLine']
            self.save()
        return name['gameName'], (name['tagLine'])
