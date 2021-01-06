import os
import sys
import webbrowser
import constants as cs
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

#from loadThread import LoadThread

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(cs.DISPLAY_TITLE + ' v' + cs.VERSION_NUM)
        self.setWindowIcon(QIcon('test.jpg'))
        self.resize(840, 512)
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        styleComboBox = QComboBox()
        styleComboBox.addItems(list(map(str, Server)))
        styleLabel = QLabel("Server:")
        styleLabel.setBuddy(styleComboBox)
        idLabel = QLabel("Riot ID:")
        self.idLineEdit = QLineEdit(self)
        #self.idLineEdit.textChanged.connect(self.idLineEditChanged)
        local.updatePlayernames('americas')

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
        self.setLayout(outerLayout)
    
    def inspectPushButtonClicked(self):
        fullname = self.idLineEdit.text().strip().split('#')
        print(fullname)
        player.inspectPlayer(fullname[0], fullname[1], self.showlog)

    def showlog(self, opponentName, outcome, deckCode):
        print('call showlog')
        htmlOpponentName = self.getHtml(opponentName ,'Black')
        htmlDeckCode = self.getHtml(deckCode, 'DarkOrange')
        htmlOutcome = self.getHtml(outcome, 'IndianRed')
        if outcome == 'win':
            htmlOutcome = self.getHtml(outcome, 'Green')
        self.textEdit.appendHtml(htmlOutcome + htmlOpponentName + htmlDeckCode)


    def getHtml(self, text, color):
        return' <font color = \"' + color + '\">' + text + '</font>'

    def idLineEditChanged(self):
        pass

setting = Setting()
setting.setServer(Server.NA)
network = Network(setting)
match = Match(network)
player = Player(match)
local = Local(setting)

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
app.setApplicationName(cs.DISPLAY_TITLE + '#')
app.setWindowIcon(QIcon('test.jpg'))
window = Window()
window.show()
sys.exit(app.exec_())