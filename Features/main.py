from riot import Riot
from network import Network
from setting import Setting, Server
from player import Player
import utility

setting = Setting()
setting.setServer(Server.EU)
network = Network(setting)
riot = Riot(network)
player = Player(riot)

# ShogoPASS#EUW
# asia europe americas


def checkPlayerDetails():
    
    puuid = riot.getPlayerPUUID('HueCicero', 'EUW')
    matchIds = riot.getMatchs(puuid)
    print(matchIds)

    winNum = 0
    matchNum = 0

    print(matchIds)

    if matchIds is None:
        print("查询失败")
        return

    tasks = [riot.aioMatchDetail(id) for id in matchIds]
    details = riot.loop.run_until_complete(riot.asyncio.gather(*tasks))
    print(details)

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
                print(str(matchNum) + ". " + riot.getPlayerName(ppid)[0])
                oppentDetails = detail['info']['players'][count]
                if oppentDetails["game_outcome"] == 'loss':
                    winNum += 1
                    outcome = 'Win'
                else:
                    outcome = 'Loss'
            else:
                myDetials = detail['info']['players'][count]
        print(outcome + "   " + str(myDetials["factions"]) + myDetials['deck_code'] + str(
            oppentDetails["factions"]) + " " + oppentDetails['deck_code'])
    print("Win rate: " + str(winNum/matchNum * 100) + "%")
    print(str(winNum) + ' out of ' + str(matchNum))


def checkPlayerDetails2(name, tag):
    puuid = riot.getPlayerPUUID(name, tag)
    matchIds = riot.getMatchs(puuid)
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
            print(details['info']['game_type'], details['info']['game_mode'],  utility.toLocalTimeString(startTime))
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
                print(str(matchNum) + ". " + riot.getPlayerName(ppid)[0] + ' ' + utility.toLocalTimeString(startTime))
                oppentDetails = details['info']['players'][count]
                if oppentDetails["game_outcome"] == 'loss':
                    winNum += 1
                    outcome = 'Win'
                else:
                    outcome = 'Loss'
            else:
                myDetials = details['info']['players'][count]
        print(outcome + "   " + str(myDetials["factions"]) + myDetials['deck_code'] + str(oppentDetails["factions"]) + " " + oppentDetails['deck_code'])
    if matchNum != 0:
        print(str(winNum) + ' wins' + ' out of ' + str(matchNum) + ' rank matchs')
        print("Win rate: " + str(int(winNum/matchNum * 100)) + "%" )
    else:
        print('无法获取对战历史数据')

checkPlayerDetails()
#checkPlayerDetails2('虎牙ace', '123')
