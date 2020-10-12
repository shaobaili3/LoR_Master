from constant import PPID_KEY
import match
import constant


matchIds = match.getMatchs(PPID_KEY)
#print(matchIds)

winNum = 0
for matchNum, matchid in enumerate(matchIds):
    details = match.getDetails(matchid)
    ppids = details['metadata']['participants']
    for count, ppid in enumerate(ppids):
        if ppid != PPID_KEY:
            print(str(matchNum + 1) + ". " + match.getPlayerName(ppid))
            oppentDetails = details['info']['players'][count]
            if oppentDetails["game_outcome"] == 'loss':
                winNum += 1
                outcome = 'Win'
            else:
                outcome = 'Loss'
            print(outcome + "   " + str(oppentDetails["factions"]) + " " + oppentDetails['deck_code'])

print("Win rate: " + str(winNum/len(matchIds) * 100) + "%" )

print(winNum)