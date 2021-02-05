from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constants as cs
import os
import sys
from setting import Setting, Server
from local import Local
from riot import Riot
from network import Network
from player import Player
from inspectorWidget import InspectorWidget
from Threads.serverThread import ServerThread
from Threads.trackThread import TrackThread
from leaderboard import getRankStr
import deck


class Window(QMainWindow):
    def __init__(self, local, player):
        super().__init__()
        self.resize(1024, 768)
        self.setWindowTitle(cs.DISPLAY_TITLE + " v" + cs.VERSION_NUM_INSPECTOR)
        self.statusBar().showMessage('LoR Disconnected')
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, cs.MAX_NUM_DETAILS + 1)
        self.progressBar.setHidden(True)
        self.player = player
        self.serverWork = ServerThread()
        self.trackWork = TrackThread()
        self.trackWork.local = local
        self.trackWork.player = player
        self.trackWork.showStatusTrigger.connect(self.showStatus)

        self.enableTrackCheckBox = QCheckBox("auto open decks")
        self.enableTrackCheckBox.setChecked(
            player.riot.network.setting.autoOpenDeck)
        self.enableTrackCheckBox.stateChanged.connect(
            self.changeEnableTrackCheckBox)

        #self.autoBrowserCheckBox = QCheckBox("Auto open opponent Decks")
        #self.autoBrowserCheckBox.setChecked(True)

        self.statusBar().addPermanentWidget(self.enableTrackCheckBox)
        #self.statusBar().addPermanentWidget(self.autoBrowserCheckBox)
        self.statusBar().addPermanentWidget(self.progressBar)

    def changeEnableTrackCheckBox(self, state):
        if state == Qt.Checked:
            self.player.riot.network.setting.autoOpenDeck = True
            self.player.riot.network.setting.saveAutoOpenDeck()
        else:
            self.player.riot.network.setting.autoOpenDeck = False
            self.player.riot.network.setting.saveAutoOpenDeck()

    def showStatus(self, text):
        self.statusBar().showMessage(text)


class Inspector(InspectorWidget):
    def __init__(self, window, setting, network, riot, player, local):
        super().__init__(setting, network, riot, player, local)
        self.parentWindow = window
        self.idLineEdit.returnPressed.connect(self.enterIdLineEdit)

    def enterIdLineEdit(self):
        if not self.inspectWork.isRunning():
            self.inspectPushButtonClicked()

    def inspectPushButtonClicked(self):
        super().inspectPushButtonClicked()
        if self.inspectWork.isRunning():
            self.inspectWork.terminate()
            self.showFinish(self.inspectWork.playerName +
                            ' inspection has been terminated')
            return

        print('inspectPushButtonClicked called')
        self.parentWindow.progressBar.setValue(1)

        fullName = self.idLineEdit.text().strip()
        self.inspectWork.playerName = fullName

        if '#' in fullName:
            # 检查名字是否过短
            if len(fullName) >= 5:
                self.inspectWork.start()
                rank = getRankStr(
                    fullName.split('#')[0], self.setting.getServer())
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
                ' is invalid, please input name and tag seperated by # eg: storm#5961',
                'OrangeRed'))
        return

    def showFinish(self, name, text):
        self.parentWindow.progressBar.setHidden(True)
        return super().showFinish(name, text)

    def showlog(self, opponentName, timeStr, outcome, deckCode, factions,
                opDeckCode, opFactions, totalTurn, num):
        self.parentWindow.progressBar.setValue(num + 1)
        return super().showlog(opponentName, timeStr, outcome, deckCode,
                               factions, opDeckCode, opFactions, totalTurn,
                               num)

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

    def showSummary(self, deckdict):
        activeWindow()
        app.alert(self)

        return super().showSummary(deckdict)

    def showMessage(self, text):
        # if text in ' match finished':
        #     print(text)
        #     playerName = text.replace(' match finished', ' [')
        #     print(playerName)
        #     self.textBrowser.append(self.getVivoHtml(playerName, 'OrangeRed') + ' match finished')

        self.textBrowser.append(self.getHtml(text, 'OrangeRed'))

    def showDecks(self, deckdict, num):
        if num == 0:
            self.textBrowser.append(
                self.getHtml('No recent rank records:', 'OrangeRed'))
            return
        activeWindow()
        app.alert(self)
        self.textBrowser.append(self.getHtml('Deck List:', 'OrangeRed'))
        for deckCode, usedTime in deckdict.items():
            #print(deckCode, usedTime)
            self.textBrowser.append(
                self.getHtml(
                    self.getHtml(
                        str(int(usedTime / num * 100)) + '%', 'Black') + ' ' +
                    deck.getChampion(deckCode), 'DarkRed') + ' ' +
                self.getDeckCodeHtml(deckCode))


def activeWindow():
    # if not window.isActiveWindow():
    if not window.isActiveWindow():
        window.showMinimized()
    window.showNormal()
    window.activateWindow()
    # window.raise_()


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
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app.setApplicationName(cs.DISPLAY_TITLE)
app.setWindowIcon(QIcon('Resource/logo.jpg'))
app.setStyle('Fusion')



window = Window(localTracker, playerTracker)
inspectorWidget = Inspector(window, settingInspect, networkInspect,
                            riotInspect, playerInspect, localInspect)
window.setCentralWidget(inspectorWidget)
window.show()
window.serverWork.setting = settingTracker
window.serverWork.start()
window.trackWork.start()

window.trackWork.showDecksTrigger.connect(inspectorWidget.showDecks)
window.trackWork.showMatchsTrigger.connect(inspectorWidget.showMatchs)
window.trackWork.showMessageTrigger.connect(inspectorWidget.showMessage)
sys.exit(app.exec())
