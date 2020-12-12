from match import Match
import requests
import network as cs

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
            if not self.isClientRuning:
                print("LoR客户端已启动")
                self.isClientRuning = True
        except requests.exceptions.RequestException as e:
            if self.isClientRuning:
                print('LoR客户端已关闭')
                self.isClientRuning = False
            return          
        details = localRequest.json()
        
        gameState = details['GameState']
        if gameState == 'InProgress':
            if self.isInProgress == False:
                print('新对局开始')
                self.isInProgress = True
            name = details['OpponentName']
            if name is not None:
                if name != self.opponentName:
                    self.opponentName = name
                    self.getTagByName(self.opponentName)
                    if self.opponentTag is None:
                        print('玩家姓名：' , self.opponentName , '，无法找到Tag')
                        return  
                    else:
                        print('已找到对手：', self.opponentName, self.opponentTag)
                        checkOpponent(self.opponentName, self.opponentTag)
        else:
            if self.isInProgress == True:
                print(self.opponentName, ' 对局结束')
                self.isInProgress = False

    def getTagByName(self, name):
        with open(cs.PLAYER_NA_PATH, encoding="utf8") as search:
            for line in search:
                fullName = line.rstrip().split('#')
                if name == fullName[0]:
                    # print(fullName)
                    self.opponentTag = fullName[1]
                    return
        print("Cannot find Opponent Tag")
        self.opponentTag = None
        return



    



