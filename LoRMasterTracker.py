from Models import leaderboard
from Threads.translateThread import TranslateThread
from Threads.serverThread import ServerThread
from Threads.trackThread import TrackThread
from Threads.uiThread import UIThread
from Models.leaderboard import updateLeaderboard
from Threads.electronThread import ElectronThread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import sys
import webbrowser
import locale

from Models.setting import Setting
from Models.local import Local
from Models.riot import Riot
from Models.network import Network
from Models.player import Player
from inspectorWidget import InspectorWidget
from leaderboardWidget import Table
from Models.leaderboard import getRankStr
from Models.leaderboard import getRankInt
import Models.deck as deck
import constants as cs
from GUI.ui import Opponent


class Window(QMainWindow):
    def __init__(self, local, player):
        super().__init__()
        self.resize(1024, 768)
        self.setWindowTitle(cs.DISPLAY_TITLE)
        # Built with ❤ by Storm/FlyingFish
        self.statusBar().showMessage(
            '[LoR Disconnected]')
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, cs.MAX_NUM_DETAILS + 1)
        self.progressBar.setHidden(True)
        self.player = player
        self.electronWork = ElectronThread()
        self.serverWork = ServerThread()
        self.trackWork = TrackThread()
        self.translateWork = TranslateThread()
        self.uiWork = UIThread()
        self.trackWork.local = local
        self.trackWork.player = player
        self.trackWork.showStatusTrigger.connect(self.showStatus)
        self.statusBar().addPermanentWidget(self.progressBar)

        self.leaderboardPushButton = QPushButton("Refresh Leaderboard")
        self.leaderboardPushButton.setDefault(True)
        self.leaderboardPushButton.clicked.connect(
            self.leaderboardPushButtonClicked)
        self.statusBar().addPermanentWidget(self.leaderboardPushButton)

        if 'zh' in locale.getdefaultlocale()[0]:
            self.translatePushButton = QPushButton("启用营地简中[不支持繁体]")
            self.translatePushButton.setDefault(True)
            self.translatePushButton.clicked.connect(
                self.translatePushButtonClicked)
            self.statusBar().addPermanentWidget(self.translatePushButton)


        self.updatePushButton = QPushButton("v" + cs.VERSION_NUM_INSPECTOR)
        self.updatePushButton.setDefault(True)
        self.updatePushButton.clicked.connect(self.updatePushButtonClicked)
        self.statusBar().addPermanentWidget(self.updatePushButton)

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        event.accept()
        app.quit()

    def leaderboardPushButtonClicked(self, state):
        leaderboard.updateAll()
        table.close()
        table.refresh()
        table.show()

    def updatePushButtonClicked(self, state):
        webbrowser.open('https://github.com/shaobaili3/LoR_Master')

    def translatePushButtonClicked(self, state):
        if self.translateWork.isRunning():
            self.translateWork.terminate()
            self.translatePushButton.setText('启用营地简中[不支持繁体]')
        else:
            self.translateWork.start()
            self.translatePushButton.setText('关闭营地简中')

    def showStatus(self, text):
        self.statusBar().showMessage(text)


class Inspector(InspectorWidget):
    def __init__(self, window, setting, network, riot, player, local):
        super().__init__(setting, network, riot, player, local)
        self.parentWindow = window
        self.idLineEdit.returnPressed.connect(self.enterIdLineEdit)
        self.textBrowser.anchorClicked.connect(self.on_anchor_clicked)
        self.deckCodeLineEdit.textChanged.connect(self.deckCodeLineTextChanged)

    def deckCodeLineTextChanged(self):
        print('deckcode line text: ', self.deckCodeLineEdit.text())
        gui.type = 'deckCode' 
        gui.deckCode = self.deckCodeLineEdit.text()
        
        if deck.validDeckCode(gui.deckCode):
            self.textBrowser.append(self.getHtml(deck.getChampion(gui.deckCode), 'ForestGreen') + self.getDeckCodeHtml(gui.deckCode) + self.getHtml(gui.deckCode, 'Black'))
        
        self.parentWindow.electronWork.start()

    def on_anchor_clicked(self, url):
        self.parentWindow.electronWork.start()
        text = url.toString()
        print(text)
        if 'deckCode' in text:
            print('open deck', text)
            gui.type = 'deckCode'            
            gui.deckCode = text.split('#')[1]
        elif 'playername' in text:
            self.inspectPlayer('#'.join(text.split('#')[2:4]))

    def inspectPlayer(self, fullName):
        if self.inspectWork.isRunning():
            self.inspectWork.terminate()
            self.showFinish(
                '', self.inspectWork.playerName +
                ' inspection has been terminated')
            return
        print('inspectPushButtonClicked called')
        self.parentWindow.progressBar.setValue(1)
        if '#' in fullName:
            # 检查名字是否过短
            if len(fullName) >= 5:
                self.inspectWork.playerName = fullName
                self.inspectWork.start()
                rank = getRankStr(
                    fullName.split('#')[0], self.setting.getServer())
                gui.matches = []
                gui.name = fullName.split('#')[0]
                gui.rank = getRankInt(
                    fullName.split('#')[0], self.setting.getServer())
                gui.type = 'match'
                self.textBrowser.append(
                    self.getHtml(fullName, 'OrangeRed') + ' ' + rank + ' (' +
                    self.setting.getServer().capitalize() + ')')
                self.textBrowser.append('')
                self.parentWindow.progressBar.setHidden(False)
                self.inspectPushButton.setText('Stop')
                return
        self.textBrowser.append(
            self.getHtml(
                fullName +
                ' is invalid, please input name and tag seperated by #  eg: storm#5961',
                'OrangeRed'))
        return

    def enterIdLineEdit(self):
        if not self.inspectWork.isRunning():
            self.inspectPushButtonClicked()

    def inspectPushButtonClicked(self):
        super().inspectPushButtonClicked()
        self.inspectPlayer(self.idLineEdit.text().strip())
        return

    def showDeckCode(self, deckCode):
        self.textBrowser.append(self.getHtml(deckCode, 'OrangeRed'))
        return

    def showFinish(self, name, text):
        self.parentWindow.progressBar.setHidden(True)
        return super().showFinish(name, text)

    def showMatchs(self, timeAgo, factions, deckCode, outcome):
        htmlFactions = self.getHtml(factions, 'OrangeRed')
        htmlOutcome = self.getHtml(outcome.capitalize(), 'IndianRed')
        if outcome == 'win':
            htmlOutcome = self.getHtml(outcome.capitalize(), 'Green')
        htmlHeros = self.getHtml(deck.getChampion(deckCode), 'DarkRed')
        htmlTimeAgo = self.getHtml(timeAgo, 'DarkOrange')
        htmlDeckCode = self.getDeckCodeHtml(deckCode)
        self.textBrowser.append(htmlOutcome + ' ' + htmlTimeAgo +
                                htmlFactions + htmlHeros + ' ' + htmlDeckCode)

    def showDetailMatch(self, opponentName, timeStr, outcome, deckCode,
                        factions, opDeckCode, opFactions, totalTurn, num):
        self.parentWindow.progressBar.setValue(num + 1)
        return super().showDetailMatch(opponentName, timeStr, outcome,
                                       deckCode, factions, opDeckCode,
                                       opFactions, totalTurn, num)

    def showSummary(self, deckdict):
        self.loadMatchsToSocket(playerInspect)

        self.textBrowser.append(self.getHtml('Summary:', 'OrangeRed'))
        for deckCode, usedTime in deckdict.items():
            #print(deckCode, usedTime)
            self.textBrowser.append(
                self.getHtml(deck.getChampion(deckCode), 'DarkRed') + ' ' +
                self.getDeckCodeHtml(deckCode) + ' ' + str(usedTime) +
                ' Games ' + self.showWinLoss(deckCode, playerInspect))
        return super().showSummary(deckdict)

    def showMessage(self, text):
        if '#' in text:
            id = text.split('#')[0]
            tag = text.split('#')[1].split('[')[0]
            gui.matches = []
            gui.name = id + '#' + tag
            gui.rank = getRankInt(id, settingTracker.getServer())
            gui.type = 'match'
            return self.textBrowser.append(
                "<a href=\"https://lor.runeterra.ar/Matches/" +
                settingTracker.riotServer.capitalize() + "/" + id + "/" + tag +
                "\" style=\"color:" + 'OrangeRed' + "\">" + text + "</a>")
        self.textBrowser.append(self.getHtml(text, 'OrangeRed'))

    def showDecks(self, deckdict, num):
        if num == 0:
            self.textBrowser.append(
                self.getHtml('No recent rank records:', 'OrangeRed'))
            return
        self.loadMatchsToSocket(playerTracker)
        self.textBrowser.append(self.getHtml('Deck List:', 'OrangeRed'))
        for deckCode, usedTime in deckdict.items():
            self.textBrowser.append(
                self.getHtml(
                    self.getHtml(
                        str(int(usedTime / num * 100)) + '%', 'Black') + ' ' +
                    deck.getChampion(deckCode), 'DarkRed') + ' ' +
                self.getDeckCodeHtml(deckCode))
        self.textBrowser.append('')

    def loadMatchsToSocket(self, player):
        gui.matches = []
        for deckCode in player.summary:
            match = {}
            match['time'] = player.summary[deckCode].time
            match['deckCode'] = deckCode
            match['matches'] = player.summary[deckCode].matches
            match['winrate'] = player.summary[
                deckCode].winNum / player.summary[deckCode].matches
            match['history'] = player.summary[deckCode].history
            gui.matches.append(match)
        self.parentWindow.electronWork.start()

    def showWinLoss(self, deckCode, player):
        winNum = player.summary[deckCode].winNum
        lossNum = player.summary[deckCode].matches - player.summary[
            deckCode].winNum
        return '[' + str(winNum) + 'W' + ' ' + str(lossNum) + 'L' + ']'

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

updateLeaderboard()

settingTracker = Setting()
networkTracker = Network(settingTracker)
riotTracker = Riot(networkTracker)
playerTracker = Player(riotTracker)
localTracker = Local(settingTracker)

settingInspect = Setting()
networkInspect = Network(settingInspect)
riotInspect = Riot(networkInspect)
playerInspect = Player(riotInspect)
localInspect = Local(settingInspect)

app = QApplication(sys.argv)

app.setAttribute(Qt.AA_UseHighDpiPixmaps)
app.setApplicationName(cs.DISPLAY_TITLE)
app.setWindowIcon(QIcon('Resource/logo.jpg'))
app.setStyle('Fusion')

#font_db = QFontDatabase()
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
font_path = os.path.join(CURRENT_DIRECTORY, "Resource", "NotoSans-Medium.ttf")
font_id = QFontDatabase.addApplicationFont(
    font_path)  # relative path is unacceptable
if font_id == -1:
    print("problem loading font")
print(font_id, QFontDatabase.applicationFontFamilies(font_id))
app.setFont(QFont(QFontDatabase.applicationFontFamilies(font_id)[0]))

window = Window(localTracker, playerTracker)
inspectorWidget = Inspector(window, settingInspect, networkInspect,
                            riotInspect, playerInspect, localInspect)
window.setCentralWidget(inspectorWidget)
window.show()
window.serverWork.setting = settingTracker
window.serverWork.start()
window.trackWork.start()
gui = Opponent('', 0, [])
window.uiWork.ui = gui
window.uiWork.start()

window.trackWork.showDecksTrigger.connect(inspectorWidget.showDecks)
window.trackWork.showMatchsTrigger.connect(inspectorWidget.showMatchs)
window.trackWork.showMessageTrigger.connect(inspectorWidget.showMessage)
app.setQuitOnLastWindowClosed(True)
table = Table()


sys.exit(app.exec())