import constants as cs
from Models.setting import Setting, Server
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
from Threads.inspectThread import InspectThread
import Models.deck as deck
from Models.leaderboard import filterMasterPlayer


class InspectorWidget(QWidget):
    def __init__(self, setting, network, riot, player, local):
        super().__init__()
        self.setting = setting
        self.network = network
        self.riot = riot
        self.player = player
        self.local = local
        self.setWindowTitle(cs.DISPLAY_TITLE + ' v' + cs.VERSION_NUM)
        #self.setWindowIcon(QIcon('test.jpg'))
        # self.resize(900, 512)
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        buttomLayout = QHBoxLayout()
        self.serverComboBox = QComboBox()
        allServers = [
            Server.NA.value.capitalize(),
            Server.EU.value.capitalize(),
            Server.ASIA.value.capitalize()
        ]
        self.serverComboBox.addItems(allServers)

        for index, oneServer in enumerate(allServers):
            if oneServer.lower() == self.setting.getServer():
                self.serverComboBox.setCurrentIndex(index)

        self.serverComboBox.activated.connect(self.changeServer)
        styleLabel = QLabel("Server:")
        styleLabel.setBuddy(self.serverComboBox)
        idLabel = QLabel("Riot ID:")
        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.setPlaceholderText('Enter name#tag here...   eg.Storm#5961')
        self.changeServer()
        self.inspectPushButton = QPushButton("Inspect")
        self.inspectPushButton.setDefault(True)
        self.inspectPushButton.clicked.connect(self.inspectPushButtonClicked)

        self.clearButton = QPushButton()
        self.clearButton.setDefault(True)
        self.clearButton.clicked.connect(self.clearButtonCliked)
        self.clearButton.setIcon(QIcon('Resource/button.png'))

        topLayout.addWidget(styleLabel)
        topLayout.addWidget(self.serverComboBox)
        topLayout.addWidget(idLabel)
        topLayout.addWidget(self.idLineEdit)
        topLayout.addWidget(self.inspectPushButton)
        topLayout.addWidget(self.clearButton)
        textLayout = QHBoxLayout()
        self.textBrowser = QTextBrowser()
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenExternalLinks(False)


        deckCodeLabel = QLabel("Deck Code: ")
        self.deckCodeLineEdit = QLineEdit(self)
        self.deckCodeLineEdit.setPlaceholderText('Enter deck code here...')
        self.importButton = QPushButton("Import Deck")
        self.importButton.clicked.connect(self.importPushButtonClicked)
        self.importButton.setDefault(True)
        buttomLayout.addWidget(deckCodeLabel)
        buttomLayout.addWidget(self.deckCodeLineEdit)
        buttomLayout.addWidget(self.importButton)

        self.textBrowser.setOpenLinks(False)
        textLayout.addWidget(self.textBrowser)
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(textLayout)
        outerLayout.addLayout(buttomLayout)
        self.setLayout(outerLayout)
        self.inspectWork = InspectThread()
        self.inspectWork.player = self.player
        self.inspectWork.showLogtrigger.connect(self.showDetailMatch)
        self.inspectWork.finishTrigger.connect(self.showFinish)
        self.inspectWork.summaryTigger.connect(self.showSummary)
        #self.textBrowser.setHtml("""My image :<br /><img src="test.ico"/  height=10 width=20>""")

    def importPushButtonClicked(self):
        textClipboard = QApplication.clipboard().text()
        self.deckCodeLineEdit.setText(textClipboard)

    def clearButtonCliked(self):
        self.textBrowser.clear()

    def inspectPushButtonClicked(self):
        return

    def showFinish(self, name, text):
        self.inspectPushButton.setText('Inspect')
        if name is None or name == "":
            self.textBrowser.append(self.getHtml(text, 'OrangeRed'))
        else:
            self.textBrowser.append(
                self.getPlayernameHtml(name, 'OrangeRed') +
                self.getHtml(text, 'OrangeRed'))
        self.textBrowser.append('')
        self.textBrowser.moveCursor(QTextCursor.MoveOperation.End)

    def showDetailMatch(self, opponentName, timeStr, outcome, deckCode,
                        factions, opDeckCode, opFactions, totalTurn, num):

        print('call showlog')
        htmlOpponentName = self.getPlayernameHtml(opponentName, 'MidnightBlue')
        htmlFactions = self.getHtml(factions, 'OrangeRed')
        htmlTotalturn = self.getHtml(' Turn: ' + totalTurn, 'DarkGray')
        htmlOpFactions = self.getHtml(opFactions, 'Black')
        htmlOutcome = self.getHtml(outcome.capitalize(), 'IndianRed')
        if outcome == 'win':
            htmlOutcome = self.getHtml(outcome.capitalize(), 'Green')
        htmlHeros = self.getHtml(deck.getChampion(deckCode), 'DarkRed')
        htmlOpHeros = self.getHtml(deck.getChampion(opDeckCode), 'black')

        self.textBrowser.append(htmlOutcome + ' ' + htmlOpponentName)
        self.textBrowser.append(
            self.getHtml(timeStr, 'DarkOrange'))
        self.textBrowser.append(htmlFactions + htmlHeros +
                                self.getDeckCodeHtml(deckCode))

        self.textBrowser.append(htmlOpFactions + htmlOpHeros +
                                self.getDeckCodeHtml(opDeckCode))

        self.textBrowser.append(htmlTotalturn)
        self.textBrowser.append(' ')

    def showSummary(self, deckdict):
        return

    def getPlayernameHtml(self, name, color):
        id = name.split('#')[0]
        tag = name.split('#')[1].split('[')[0]
        return "<a href=\"playername#" + self.setting.riotServer.capitalize(
        ) + "#" + id + "#" + tag + "\" style=\"color:" + color + "\">" + name + "</a>"
    def getDeckCodeHtml(self, text):
        return "<a href=\"deckCode#" + text + "\" style=\"color:DodgerBlue\">" + 'View Deck' + "</a>"

    def getHtml(self, text, color):
        return ' <font color = \"' + color + '\">' + text + '</font>'

    def changeServer(self):
        serverName = self.serverComboBox.currentText().lower()
        print('changeSever call')
        #completer = QCompleter(local.playernames)
        self.setting.setServer(Server._value2member_map_[serverName])
        self.setting.saveServer()
        self.local.updatePlayernames()
        completer = QCompleter(
            filterMasterPlayer(self.local.playernames, serverName))
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.idLineEdit.setCompleter(completer)
        self.idLineEdit.setText('')