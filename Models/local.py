import requests
from Models.setting import Server
import constants as cs
import Models.utility as utility
from Models.leaderboard import getRankStr, updateLeaderboard


class Local:
    def __init__(self, setting):
        self.opponentName = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False
        self.setting = setting
        self.playernames = set()
        self.playername = None
        #self.updatePlayernames()

    # call this function after changes server in the tracker
    def reset(self):
        self.opponentName = None
        self.playername = None
        self.opponentTag = None
        self.isClientRuning = False
        self.isInProgress = False

    def updateStatus(self, checkOpponent, showMessage, showStatus, showMatchs,
                     showDecks):
        try:
            localRequest = requests.get(self.getLocalLink())
            if not self.isClientRuning:
                # LoR client launched
                print('LoR客户端已启动', '当前服务器:', self.setting.getServer())
                showStatus('[LoR Connected: ' + self.setting.getServer() + ']')
                self.isClientRuning = True
        except requests.exceptions.RequestException:
            if self.isClientRuning:
                print('LoR客户端已关闭')  # LoR client exited
                showStatus('[LoR Disconnected]')
                self.isClientRuning = False
                self.reset()
            return
        try:
            details = localRequest.json()
        except ValueError:
            print('Decoding local port json failed')
            return
        gameState = details['GameState']
        vsPlayerStr = ''
        if gameState == 'InProgress':
            if not self.isInProgress:
                print('新对局开始')  # New Match Found
                self.isInProgress = True
            opName = details['OpponentName']
            playerName = details['PlayerName']
            if opName:
                if opName != self.opponentName:
                    if not playerName:
                        return
                    vsPlayerStr = getRankStr(opName.strip(
                    ), self.setting.getServer()) + ' vs ' + playerName.strip()
                    showStatus(
                        opName + ' ' + vsPlayerStr + ' ' +
                        getRankStr(playerName, self.setting.getServer()))

                    self.opponentName = opName
                    self.updateTagByName(self.opponentName)
                    showMessage(
                        opName + ' ' + vsPlayerStr + ' ' +
                        getRankStr(playerName, self.setting.getServer()))
                    if self.opponentTag is None:
                        # Play Tag does not exist
                        print('玩家姓名：', self.opponentName, '，无法找到Tag')
                        showMessage('Cannot find opponent tag')
                        showMessage('')
                        return
                    else:
                        # Opponent tag found:
                        print('发现对手：', self.opponentName, '#',
                              self.opponentTag, "正在载入卡组...")
                        showMessage(self.opponentName + '#' + self.opponentTag)
                        checkOpponent(self.opponentName, self.opponentTag,
                                      showMessage, showMatchs, showDecks)
        else:
            if self.isInProgress:
                if None not in (self.opponentName, self.opponentTag):
                    print(self.opponentName, '#', self.opponentTag, ' 对局结束')
                    # showMessage(self.opponentName + '#' + self.opponentTag + ' match finished')
                    showMessage('')
                self.reset()
                showStatus('LoR Connected: ' + self.setting.getServer())
                updateLeaderboard()

    def updateTagByName(self, name):
        with open(('Resource/' + self.setting.getServer() + '.dat'),
                  encoding="utf8") as search:
            for line in search:
                fullName = line.rstrip().split('#')
                if name == fullName[0]:
                    # print(fullName)
                    self.opponentTag = fullName[1]
                    return
        self.opponentTag = None

    def updatePlayernames(self):
        self.playernames = set()
        #with open(utility.resource_path('Resource/' + self.setting.getServer() + '.dat'), encoding="utf8") as search:
        with open(('Resource/' + self.setting.getServer() + '.dat'),
                  encoding="utf8") as search:
            for line in search:
                fullName = line.strip()
                self.playernames.add(fullName)

    def getLocalLink(self):
        return cs.IP_KEY + self.setting.getPort() + cs.LOCAL_KEY
