import requests
import aiohttp
import asyncio


class Riot:
    def __init__(self, network):
        self.network = network
        self.asyncio = asyncio
        self.loop = None
        return

    def getPlayerPUUID(self, name, tag):
        puuidLink = self.network.getPUUID(name, tag)
        # print(puuidLink)
        try:
            puuidRequest = requests.get(puuidLink)
        except requests.exceptions.RequestException as e:
            print(puuidLink)
            print(e)
            print('无法连接PUUID服务器')
            return None
        idDetails = puuidRequest.json()
        if not puuidRequest.ok:
            print(puuidLink)
            print(puuidRequest.headers)
            print(puuidRequest.status_code)
            print('userId -> PUUID服务器错误')
            print(idDetails)
            return None
        return idDetails.get('puuid')

    def getMatchs(self, ppid):
        matchLink = self.network.getMatchsLink(ppid)
        try:
            matchRequest = requests.get(matchLink)
        except requests.exceptions.RequestException as e:
            print(matchLink)
            print(e)
            print('无法连接比赛ID服务器')
            return None
        matchIds = matchRequest.json()
        if not matchRequest.ok:
            print(matchLink)
            print(matchRequest.headers)
            print(matchRequest.status_code)
            print('比赛ID服务器错误')
            print(matchIds)
            return None
        return matchIds

    async def aioMatchDetail(self, id):
        async with aiohttp.ClientSession() as session:
            detailsLink = self.network.getDetailsLink(id)
            async with session.get(detailsLink) as resp:
                detail = await resp.json()

        header = resp.headers
        if 'X-Method-Rate-Limit-Count' in header:
            print('X-Method-Rate-Limit-Count: ',
                  header['X-Method-Rate-Limit-Count'])
            print('X-App-Rate-Limit', header['X-App-Rate-Limit'])

        if 'Retry-After' in header:
                print('aio服务器正忙,请等待', header['Retry-After'], '秒')
                return header['Retry-After']

        if resp.ok:
            return detail
        else:
            print('AIO比赛内容服务器错误: ', resp.status)
            print(detailsLink)
            print(detail)
            return None

    def getDetail(self, matchId):
        detailsLink = self.network.getDetailsLink(matchId)
        try:
            detailsRequest = requests.get(detailsLink)
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
                return header['Retry-After']
            return None
        if detail is None:
            print('比赛内容服务返回空')
        return detail

    # 在main中使用和inspector中使用
    def getPlayerName(self, puuid):
        nameLink = self.network.getNameLink(puuid)
        try:
            nameRequest = requests.get(nameLink)
        except requests.exceptions.RequestException as e:
            print(nameLink)
            print(e)
            print('无法连接puuid->userId服务器')
            return '名字Unknow', 'unknow'
        name = nameRequest.json()
        #headers = nameRequest.headers
        #print(headers)
        if not nameRequest.ok:
            print(nameLink)
            print(nameRequest.headers)
            print(nameRequest.status_code)
            print(name)
            print('puuid->userid服务器错误:')
            return '名字Unknow', 'unknow'
        return name['gameName'], name['tagLine']


# setting = Setting()
# network = Network(setting)
# riot = Riot(network)
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# tasks = [riot.aioLeaderboard(server) for server in [Server.NA.value, Server.EU.value, Server.ASIA.value]]
# ap = loop.run_until_complete(riot.asyncio.gather(*tasks))

# for aps in ap:
#     if aps is None:
#         print('lolololol')
