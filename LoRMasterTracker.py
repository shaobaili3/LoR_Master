from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constants as cs
import os
import sys
from setting import Setting
from local import Local
from riot import Riot
from network import Network
from player import Player
from inspectorWidget import InspectorWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1024, 768)
        self.statusBar().showMessage("v" + cs.VERSION_NUM_INSPECTOR)
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, cs.MAX_NUM_DETAILS)
        self.progressBar.setHidden(True)
        self.statusBar().addPermanentWidget(self.progressBar)


class Inspector(InspectorWidget):
    def __init__(self, window, setting, network, riot, player, local):
        super().__init__(setting, network, riot, player, local)
        self.parentWindow = window

        if not self.inspectWork.isRunning():
            self.trackWork.start()

    def inspectPushButtonClicked(self):
        super().inspectPushButtonClicked()
        if self.inspectWork.isRunning():
            self.inspectWork.terminate()
            self.showFinish(self.inspectWork.playerName +
                            ' inspection has been terminated')
            return

        print('inspectPushButtonClicked called')
        self.parentWindow.progressBar.setValue(0)

        fullName = self.idLineEdit.text().strip()
        self.inspectWork.playerName = fullName

        if '#' in fullName:
            # 检查名字是否过短
            if len(fullName) >= 5:
                self.inspectWork.start()
                rank = self.riot.getRankStr(
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

    def showFinish(self, text):
        self.parentWindow.progressBar.setHidden(True)
        return super().showFinish(text)

    def showlog(self, opponentName, timeStr, outcome, deckCode, factions,
                opDeckCode, opFactions, totalTurn, num):
        self.parentWindow.progressBar.setValue(num)
        return super().showlog(opponentName, timeStr, outcome, deckCode,
                               factions, opDeckCode, opFactions, totalTurn,
                               num)


setting = Setting()
network = Network(setting)
riot = Riot(network)
player = Player(riot)
local = Local(setting)
app = QApplication(sys.argv)
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app.setApplicationName(cs.DISPLAY_TITLE)
app.setWindowIcon(QIcon('Resource/logo.jpg'))
app.setStyle('Fusion')
window = Window()
inspectorWidget = Inspector(window, setting, network, riot, player, local)
window.setCentralWidget(inspectorWidget)
window.show()
sys.exit(app.exec())