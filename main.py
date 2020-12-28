from match import Match
from network import Network
from setting import Setting, Server
from opponent import Opponent

setting = Setting()
setting.setServer(Server.EU)
network = Network(setting)
match = Match(network)
opponent = Opponent(match)

#ShogoPASS#EUW
puuid = match.getPlayerPUUID('ShogoPASS', 'EUW')
#asia europe americas



def checkPlayerDetails():
    matchIds = match.getMatchs(puuid)
    print(matchIds)

    winNum = 0
    matchNum = 0

    print(matchIds)

    if matchIds is None:
        print("查询失败")
        return

    tasks = [match.aioGetDetail(id) for id in matchIds]
    details = match.loop.run_until_complete(match.asyncio.gather(*tasks))
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
                #print(ppid)
                print(str(matchNum) + ". " + match.getPlayerName(ppid))
                oppentDetails = detail['info']['players'][count]
                if oppentDetails["game_outcome"] == 'loss':
                    winNum += 1
                    outcome = 'Win'
                else:
                    outcome = 'Loss'
            else:
                myDetials = detail['info']['players'][count]
        print(outcome + "   " + str(myDetials["factions"]) + myDetials['deck_code'] + str(oppentDetails["factions"]) + " " + oppentDetails['deck_code'])
    print("Win rate: " + str(winNum/matchNum * 100) + "%" )
    print(str(winNum) + ' out of ' + str(matchNum))


# def checkPlayerDetails():
#     matchIds = match.getMatchs(puuid)
#     print(matchIds)

#     winNum = 0
#     matchNum = 0

#     print(matchIds)

#     if matchIds is None:
#         print("查询失败")
#         return
#     for matchid in matchIds:
#         details = match.getDetail(matchid)
#         if details is None:
#             continue
#         if details['info']['game_type'] != 'Ranked':
#             continue
#         else:
#             matchNum += 1
#         ppids = details['metadata']['participants']
#         outcome = None
#         oppentDetails = None
#         myDetials = None
#         for count, ppid in enumerate(ppids):
#             if ppid != puuid:
#                 #print(ppid)
#                 print(str(matchNum) + ". " + match.getPlayerName(ppid))
#                 oppentDetails = details['info']['players'][count]
#                 if oppentDetails["game_outcome"] == 'loss':
#                     winNum += 1
#                     outcome = 'Win'
#                 else:
#                     outcome = 'Loss'
#             else:
#                 myDetials = details['info']['players'][count]
#         print(outcome + "   " + str(myDetials["factions"]) + myDetials['deck_code'] + str(oppentDetails["factions"]) + " " + oppentDetails['deck_code'])
#     print("Win rate: " + str(winNum/matchNum * 100) + "%" )
#     print(str(winNum) + ' out of ' + str(matchNum))

#opponent.checkOpponent('Storm', '5961')
checkPlayerDetails()

