import requests
from setting import Server
import constants as cs


class Local:
    def __init__(self, setting):
        self.opponentName = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False
        self.setting = setting

    def reset(self):
        self.opponentName = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False

    def updateStatus(self, checkOpponent):
        try:
            localRequest = requests.get(self.getLocalLink())
            if not self.isClientRuning:
                # LoR client lanuched
                print('LoR客户端已启动', '当前服务器:', self.setting.getServer())
                self.isClientRuning = True
        except requests.exceptions.RequestException as e:
            if self.isClientRuning:
                print('LoR客户端已关闭')  # LoR client exited
                self.isClientRuning = False
            return
        details = localRequest.json()
        gameState = details['GameState']
        if gameState == 'InProgress':
            if self.isInProgress == False:
                print('新对局开始')  # New Match Found
                self.isInProgress = True
            name = details['OpponentName']
            if name is not None:
                if name != self.opponentName:
                    self.opponentName = name
                    self.getTagByName(self.opponentName)
                    if self.opponentTag is None:
                        # Play Tag does not exist
                        print('玩家姓名：', self.opponentName, '，无法找到Tag')
                        return
                    else:
                        # Opponent tag found:
                        print('发现对手：', self.opponentName, '#',
                              self.opponentTag, "正在载入卡组...")
                        checkOpponent(self.opponentName, self.opponentTag)
        else:
            if self.isInProgress == True:
                print(self.opponentName, '#', self.opponentTag, ' 对局结束')
                self.isInProgress = False

    def getTagByName(self, name):
        print(name)
        print(self.setting.getServer())
        with open(('Resource/' + self.setting.getServer() + '.dat'), encoding="utf8") as search:
            for line in search:
                fullName = line.rstrip().split('#')
                if name == fullName[0]:
                    # print(fullName)
                    self.opponentTag = fullName[1]
                    return self.opponentTag
        print("Cannot find Opponent Tag")
        self.opponentTag = None
        return self.opponentTag

    def getLocalLink(self):
        return cs.IP_KEY + self.setting.getPort() + cs.LOCAL_KEY
