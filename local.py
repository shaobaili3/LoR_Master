import constant as cs
import requests

class Local:    
    
    def __init__(self):
        self.opponentName = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False

    def updateStatus(self, checkOpponent):
        localLink = cs.geLocalLink(cs.PORT_NUM)
        try:
            localRequest = requests.get(localLink)
            self.isClientRuning = True
        except requests.exceptions.RequestException as e:
            self.isClientRuning = False
            return          
        details = localRequest.json()
        
        gameState = details['GameState']
        if gameState == 'InProgress':
            isInProgress = True
            name = details['OpponentName']
            if name is not None:
                if name != self.opponentName:
                    self.opponentName = name
                    self.getTagByName(self.opponentName)

                    print(self.opponentName, self.opponentTag)
                    checkOpponent(self.opponentName, self.opponentTag)
        else:
            isInProgress = False

    def getTagByName(self, name):
        with open(cs.PLAYER_NA_PATH, encoding="utf8") as search:
            for line in search:
                fullName = line.rstrip().split('#')
                if name == fullName[0]:
                    # print(fullName)
                    self.opponentTag = fullName[1]
                    return
        print("Cannot find Opponent Tag")
        return


    #def statusListener(checkOpponent()):





# def getOpponentName():
#     localLink = cs.geLocalLink(cs.PORT_NUM)
#     try:
#         localRequest = requests.get(localLink)



#     except requests.exceptions.RequestException as e:
#         # print("Connection Error:", e)
#         print("游戏未启动")
#         return "Missing Client 3"  
#     details = localRequest.json()
#     #print(details)
#     return details['OpponentName']



    



