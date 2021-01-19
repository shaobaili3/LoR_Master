import constants as cs
import os
from setting import Setting, Server
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui

from local import Local
from riot import Riot
from network import Network
from player import Player
from inspectThread import InspectThread
from trackThread import TrackThread
import deck

class InspectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setting = Setting()
        self.network = Network(self.setting)
        self.riot = Riot(self.network)
        self.player = Player(self.riot)
        self.local = Local(self.setting)
        self.setWindowTitle(cs.DISPLAY_TITLE + ' v' + cs.VERSION_NUM)
        #self.setWindowIcon(QIcon('test.jpg'))
        # self.resize(900, 512)
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        styleComboBox = QComboBox()
        allServers = [Server.NA.value, Server.EU.value, Server.ASIA.value]
        styleComboBox.addItems(allServers)
        for index, oneServer in enumerate(allServers):
            if oneServer == self.setting.getServer():
                styleComboBox.setCurrentIndex(index)
            self.local.updatePlayernames()
        styleComboBox.activated[str].connect(self.changeServer)
        styleLabel = QLabel("Server:")
        styleLabel.setBuddy(styleComboBox)
        idLabel = QLabel("Riot ID:")
        self.idLineEdit = QLineEdit(self)
        # self.idLineEdit.textChanged.connect(self.idLineEditChanged)
        completer = QCompleter(self.local.playernames)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.idLineEdit.setCompleter(completer)
        self.inspectPushButton = QPushButton("Inspect")
        self.inspectPushButton.setDefault(True)
        self.inspectPushButton.clicked.connect(self.inspectPushButtonClicked)


        self.clearButton = QPushButton()
        self.clearButton.setDefault(True)
        self.clearButton.clicked.connect(self.clearButtonCliked)
        self.clearButton.setIcon(QIcon('Resource/button.png'))

        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addWidget(idLabel)
        topLayout.addWidget(self.idLineEdit)
        topLayout.addWidget(self.inspectPushButton)
        topLayout.addWidget(self.clearButton)
        textLayout = QHBoxLayout()
        self.textBrowser = QTextBrowser()
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenExternalLinks(True)
        textLayout.addWidget(self.textBrowser)
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(textLayout)
        self.setLayout(outerLayout)
        self.inspectWork = InspectThread()
        self.inspectWork.player = self.player
        self.inspectWork.showLogtrigger.connect(self.showlog)
        self.inspectWork.finishTrigger.connect(self.showFinish)
        self.inspectWork.summaryTigger.connect(self.showSummary)

        self.trackWork = TrackThread()
        self.trackWork.local = self.local
        self.trackWork.player = self.player

        #self.textBrowser.setHtml("""My image :<br /><img src="test.ico"/  height=10 width=20>""")

    def clearButtonCliked(self):
        self.textBrowser.clear()
    
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
        self.inspectPushButton.setText('Inspect')
        if text is None:
            pass
        else:
            self.textBrowser.append(self.getHtml(text, 'OrangeRed'))
            #为了美观最后空一行
            self.textBrowser.append('')
        self.textBrowser.moveCursor(QTextCursor.End)
        


    def showlog(self, opponentName, timeStr, outcome, deckCode, factions,opDeckCode, opFactions, totalTurn, num):

        print('call showlog')
        htmlOpponentName = self.getHtml(opponentName, 'Black')
        htmlOutcome = self.getHtml(outcome.capitalize(), 'IndianRed')
        htmlFactions = self.getHtml(factions, 'OrangeRed')
        htmlTotalturn = self.getHtml('Turn: ' + str(totalTurn), 'DarkGray')
        htmlopFactions = self.getHtml(opFactions, 'Black')
        if outcome == 'win':
            htmlOutcome = self.getHtml(outcome.capitalize(), 'Green')

        htmlHeros = self.getHtml(deck.getChampion(deckCode), 'DarkRed')
        htmlOpHeros = self.getHtml(deck.getChampion(opDeckCode), 'black')

        self.textBrowser.append(htmlOutcome + htmlOpponentName) 
        self.textBrowser.append(self.getHtml(timeStr, 'DarkOrange') + ' ' + htmlTotalturn)
        self.textBrowser.append(htmlFactions + htmlHeros)
        self.textBrowser.append(self.getDeckCodeHtml(deckCode))
        
        self.textBrowser.append(htmlopFactions + htmlOpHeros)
        self.textBrowser.append(self.getDeckCodeHtml(opDeckCode))
        self.textBrowser.append(' ')


    def showSummary(self, deckdict):
        self.textBrowser.append(self.getHtml('Summary:' , 'OrangeRed'))
        for deckCode, usedTime in deckdict.items():
            #print(deckCode, usedTime)
            self.textBrowser.append(self.getHtml(deck.getChampion(deckCode), 'DarkRed') + ' ' + self.getDeckCodeHtml(deckCode) + ' ' + str(usedTime) + ' times')
        self.textBrowser.append('')

    def getDeckCodeHtml(self, text):
        return "<a href=\"https://lor.mobalytics.gg/decks/code/" + text + "\">" + text + "</a>"

    def getHtml(self, text, color):
        return' <font color = \"' + color + '\">' + text + '</font>'
    
    def changeServer(self, serverName):
        print('changeSever call')
        #completer = QCompleter(local.playernames)
        self.setting.setServer(Server._value2member_map_[serverName])
        self.local.updatePlayernames()
        completer = QCompleter(self.local.playernames)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.idLineEdit.setCompleter(completer)
        self.idLineEdit.setText('')



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
