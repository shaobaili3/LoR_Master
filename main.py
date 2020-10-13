from constant import PPID_KEY
import match
import constant


matchIds = match.getMatchs(PPID_KEY)
#print(matchIds)

winNum = 0
matchNum = 0
for matchNum, matchid in enumerate(matchIds):
    details = match.getDetails(matchid)
    if details['info']['game_type'] != 'Ranked':
        continue
    else:
        matchNum += 1
    ppids = details['metadata']['participants']
    for count, ppid in enumerate(ppids):
        if ppid != PPID_KEY:
            #print(ppid)
            print(str(matchNum + 1) + ". " + match.getPlayerName(ppid))
            oppentDetails = details['info']['players'][count]
            if oppentDetails["game_outcome"] == 'loss':
                winNum += 1
                outcome = 'Win'
            else:
                outcome = 'Loss'
            print(outcome + "   " + str(oppentDetails["factions"]) + " " + oppentDetails['deck_code'])

print("Win rate: " + str(winNum/matchNum * 100) + "%" )

print(str(winNum) + ' out of ' + str(matchNum))