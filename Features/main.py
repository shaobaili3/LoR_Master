from Models.leaderboard import Leaderboard
from Models.setting import Setting
from Models.local import Local
from Models.riot import Riot
from Models.network import Network
from Models.player import Player
from Models.setting import Server
from Models.cache import Cache

setting = Setting()
network = Network(setting)
riot = Riot(network, Cache())
# J01#EU1
# asia europe americas


def checkPlayerDetails():

    puuid = riot.getPlayerPUUID('storm', '5961')
    matchIds = riot.getMatches(puuid)
    print(matchIds)

    winNum = 0
    matchNum = 0

    #print(matchIds)

    if matchIds is None:
        print("查询失败")
        return
    loop = riot.asyncio.new_event_loop()
    riot.asyncio.set_event_loop(loop)
    tasks = [riot.aioMatchDetail(id) for id in matchIds]
    details = loop.run_until_complete(riot.asyncio.gather(*tasks))
    #print(details)

    for detail in details:
        if detail is None:
            continue
        if detail['info']['game_type'] != 'Ranked':
            continue
        else:
            matchNum += 1
        ppids = detail['metadata']['participants']
        outcome = None
        oppentDetails = None
        myDetials = None
        for count, ppid in enumerate(ppids):
            if ppid != puuid:
                # print(ppid)
                #print(str(matchNum) + ". " + riot.getPlayerName(ppid)[0])
                oppentDetails = detail['info']['players'][count]
                if oppentDetails["game_outcome"] == 'loss':
                    winNum += 1
                    outcome = 'Win'
                else:
                    outcome = 'Loss'
            else:
                myDetials = detail['info']['players'][count]
        print(outcome + "   " + str(myDetials["factions"]) +
              myDetials['deck_code'] + str(oppentDetails["factions"]) + " " +
              oppentDetails['deck_code'])
    print("Win rate: " + str(winNum / matchNum * 100) + "%")
    print(str(winNum) + ' out of ' + str(matchNum))


def checkPlayerDetails2(name, tag):
    puuid = riot.getPlayerPUUID(name, tag)
    matchIds = riot.getMatches(puuid)
    winNum = 0
    matchNum = 0
    if matchIds is None:
        print("查询失败")
        return
    for matchid in matchIds:
        if matchNum == 5:
            break
        details = match.getDetail(matchid)

        if details is None:
            continue

        startTime = details['info']['game_start_time_utc']
        if details['info']['game_type'] != 'Ranked':
            print(details['info']['game_type'], details['info']['game_mode'],
                  utility.toLocalTimeString(startTime))
            continue
        else:
            matchNum += 1
        ppids = details['metadata']['participants']
        outcome = None
        oppentDetails = None
        myDetials = None
        for count, ppid in enumerate(ppids):
            if ppid != puuid:
                #print(ppid)
                print(
                    str(matchNum) + ". " + riot.getPlayerName(ppid)[0] + ' ' +
                    utility.toLocalTimeString(startTime))
                oppentDetails = details['info']['players'][count]
                if oppentDetails["game_outcome"] == 'loss':
                    winNum += 1
                    outcome = 'Win'
                else:
                    outcome = 'Loss'
            else:
                myDetials = details['info']['players'][count]
        print(outcome + "   " + str(myDetials["factions"]) +
              myDetials['deck_code'] + str(oppentDetails["factions"]) + " " +
              oppentDetails['deck_code'])
    if matchNum != 0:
        print(
            str(winNum) + ' wins' + ' out of ' + str(matchNum) +
            ' rank matchs')
        print("Win rate: " + str(int(winNum / matchNum * 100)) + "%")
    else:
        print('无法获取对战历史数据')


checkPlayerDetails()
#checkPlayerDetails2('虎牙ace', '123')
