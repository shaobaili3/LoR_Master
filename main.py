from match import Match
from network import Network

network = Network('americas')
match = Match(network)

puuid = match.getPlayerPUUID('Storm', '5961')
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
    for matchid in matchIds:
        details = match.getDetails(matchid)
        if details is None:
            continue
        if details['info']['game_type'] != 'Ranked':
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
                print(str(matchNum) + ". " + match.getPlayerName(ppid))
                oppentDetails = details['info']['players'][count]
                if oppentDetails["game_outcome"] == 'loss':
                    winNum += 1
                    outcome = 'Win'
                else:
                    outcome = 'Loss'
            else:
                myDetials = details['info']['players'][count]
        print(outcome + "   " + str(myDetials["factions"]) + myDetials['deck_code'] + str(oppentDetails["factions"]) + " " + oppentDetails['deck_code'])
    print("Win rate: " + str(winNum/matchNum * 100) + "%" )
    print(str(winNum) + ' out of ' + str(matchNum))

checkPlayerDetails()
