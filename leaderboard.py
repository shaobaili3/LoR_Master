from setting import Server
import aiohttp
import asyncio
from network import API_KEY

leaderboards = [None, None, None, None]
LEADERBOARD_KEY = '.api.riotgames.com/lor/ranked/v1/leaderboards/'


def updateLeaderboard():
    if None in leaderboards:
        updateAll()
    if None in leaderboards:
        updateAll()


def updateAll():
    # loop = self.asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [
        aioLeaderboard(server) for server in
        [Server.NA.value, Server.EU.value, Server.ASIA.value, 'sea']
    ]
    boards = loop.run_until_complete(asyncio.gather(*tasks))
    for index, board in enumerate(boards):
        if board is not None:
            leaderboards[index] = board


def checkRank(name, server):
    rank = ''
    lp = ''

    print('rank search:', name, server)

    if None in leaderboards:
        updateAll()

    board = None
    if server == Server.NA.value:
        ab = leaderboards[0]
        if ab:
            board = ab.get('players')
    if server == Server.EU.value:
        ab = leaderboards[1]
        if ab:
            board = ab.get('players')
    elif server == Server.ASIA.value:
        ab = leaderboards[2]
        if ab:
            board = ab.get('players')
    elif server == 'sea':
        ab = leaderboards[3]
        if ab:
            board = ab.get('players')
    if not board:
        return rank, lp

    for playerRank in board:
        if playerRank['name'] == name:
            rank = str(playerRank['rank'] + 1)
            lp = str(int(playerRank['lp']))
    return rank, lp


def getRankStr(name, server):
    rank, lp = checkRank(name, server)
    if rank != '':
        return '[Rank: ' + rank + ' lp: ' + lp + ']'
    else:
        return ''


async def aioLeaderboard(server):
    async with aiohttp.ClientSession() as session:
        link = getLeaderboard(server)
        try:
            async with session.get(link) as resp:
                # print(resp.status)
                detail = await resp.json()
        except aiohttp.ClientConnectionError as e:
            print('aioLeaderboard Error: ', str(e))
            return None

    print('status:', resp.status)
    if resp.ok:
        return detail
    else:
        print('排行榜服务器错误: ', server, resp.status)
        print(detail)
        return None


def getLeaderboard(server):
    return 'https://' + server + LEADERBOARD_KEY + API_KEY
