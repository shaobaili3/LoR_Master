import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import match
import constant
from match import getDetails, getPlayerPUUID


# Use a service account

def initialFirebase():
    # Use a service account
    cred = credentials.Certificate('lor-master-firebase-adminsdk-zgtn7-21c20de161.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db



def writeMatchs(name, tag):
    puuid = getPlayerPUUID(name, tag)
    matchIds = match.getMatches(puuid)
    print(matchIds)
    for matchId in matchIds:
        print('*')
        print(matchId)
        doc = db.collection(u'players').document(puuid).collection(u'matchs').document(matchId).get()
        if doc.exists:
            print(f'Document data: {doc.to_dict()}')
            break
        else:
            print(u'No such document!')
        details = getDetails(matchId)
        # print(details)
        # print(matchId)
        if details['info']['game_type'] == 'Ranked': 
            db.collection(u'players').document(puuid).collection(u'matchs').document(matchId).set(details)


def readMatchs(name, tag):
    puuid = getPlayerPUUID(name, tag)
    print(puuid)
    docs = db.collection(u'players').document(puuid).collection(u'matchs').stream()

    winNum = 0
    matchNum = 0
    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()}')
        details = doc.to_dict()
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


db = initialFirebase()
writeMatchs('storm', '5961')
readMatchs('storm', '5961')



# data = {
#     u'stringExample': u'Hello, World!',
#     u'booleanExample': True,
#     u'numberExample': 3.14159265,
#     u'arrayExample': [5, True, u'hello'],
#     u'nullExample': None,
#     u'objectExample': {
#         u'a': 5,
#         u'b': True
#     }
# }

# db.collection(u'data').document(u'one').set(data)