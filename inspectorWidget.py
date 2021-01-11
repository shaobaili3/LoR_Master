import constants as cs
import os
from setting import Setting, Server
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui

from local import Local
from match import Match
from network import Network
from player import Player
from loadThread import LoadThread


class InspectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle(cs.DISPLAY_TITLE + ' v' + cs.VERSION_NUM)
        # self.setWindowIcon(QIcon('test.jpg'))
        # self.resize(900, 512)
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        styleComboBox = QComboBox()
        allServers = [Server.NA.value, Server.EU.value, Server.ASIA.value]
        styleComboBox.addItems(allServers)
        for index, oneServer in enumerate(allServers):
            if oneServer == setting.getServer():
                styleComboBox.setCurrentIndex(index)
            local.updatePlayernames()
        styleComboBox.activated[str].connect(self.changeServer)
        styleLabel = QLabel("Server:")
        styleLabel.setBuddy(styleComboBox)
        idLabel = QLabel("Riot ID:")
        self.idLineEdit = QLineEdit(self)
        # self.idLineEdit.textChanged.connect(self.idLineEditChanged)
        completer = QCompleter(local.playernames)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.idLineEdit.setCompleter(completer)
        self.inspectPushButton = QPushButton("Inspect")
        self.inspectPushButton.setDefault(True)
        self.inspectPushButton.clicked.connect(self.inspectPushButtonClicked)
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addWidget(idLabel)
        topLayout.addWidget(self.idLineEdit)
        topLayout.addWidget(self.inspectPushButton)
        textLayout = QHBoxLayout()
        self.textEdit = QPlainTextEdit()
        self.textEdit.setReadOnly(True)
        textLayout.addWidget(self.textEdit)
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(textLayout)

        # buttomLayout = QVBoxLayout()
        # self.progressBar = QProgressBar()
        # self.progressBar.setRange(0, 5)
        # self.progressBar.setValue(1)
        # buttomLayout.addWidget(self.progressBar)
        # outerLayout.addLayout(buttomLayout)

        self.setLayout(outerLayout)
        self.work = LoadThread()
        self.work.player = player
        self.work.trigger.connect(self.showlog)
        self.work.finishTrigger.connect(self.showFinish)

    def inspectPushButtonClicked(self):
        pass
        # print('start button pushed')
        # fullName = self.idLineEdit.text().strip()
        # self.work.plaerName = fullName
        

        # if '#' in fullName:
        #     if len(fullName) >= 5:
        #         self.work.start()
        #         self.textEdit.appendHtml(self.getHtml(fullName, 'OrangeRed'))
        #         return
        
        # self.textEdit.appendHtml(self.getHtml(fullName + ' is invalid, please input name and tag seperated by # eg: storm#5961', 'OrangeRed')) 

    def showFinish(self, text):
        if text is None:
            pass
        else:
            self.textEdit.appendHtml(self.getHtml(text, 'OrangeRed'))


    def showlog(self, opponentName, outcome, deckCode, factions,opDeckCode, opFactions, totalTurn, num):

        print('call showlog')
        htmlOpponentName = self.getHtml(opponentName, 'Black')
        htmlDeckCode = self.getHtml(deckCode, 'DarkOrange')
        htmlOutcome = self.getHtml(outcome, 'IndianRed')
        htmlFactions = self.getHtml(factions, 'Black')
        htmlTotalturn = self.getHtml('Turn: ' + str(totalTurn), 'Gold')
        htmlopDeckCode = self.getHtml(opDeckCode, 'DarkOrange')
        htmlopFactions = self.getHtml(opFactions, 'Black')
        if outcome == 'win':
            htmlOutcome = self.getHtml(outcome, 'Green')
        self.textEdit.appendHtml(htmlOutcome + htmlOpponentName + htmlTotalturn)
        self.textEdit.appendHtml(htmlFactions + htmlDeckCode)
        self.textEdit.appendHtml(htmlopFactions + htmlopDeckCode)
        self.textEdit.appendHtml(' ')

    def getHtml(self, text, color):
        return' <font color = \"' + color + '\">' + text + '</font>'

    def changeServer(self, serverName):
        print('changeSever call')
        #completer = QCompleter(local.playernames)
        setting.setServer(Server._value2member_map_[serverName])
        local.updatePlayernames()
        completer = QCompleter(local.playernames)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.idLineEdit.setCompleter(completer)
        self.idLineEdit.setText('')


setting = Setting()
network = Network(setting)
match = Match(network)
player = Player(match)
local = Local(setting)
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
#os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# app = QApplication(sys.argv)
# app.setApplicationName(cs.DISPLAY_TITLE + '#')
# app.setWindowIcon(QIcon('test.jpg'))
# app.setStyle('Fusion')
# window = InspectorWidget()
# window.show()
# print(QStyleFactory.keys())
#sys.exit(app.exec_())
