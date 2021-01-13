from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constants as cs
import os
import sys
from inspectorWidget import InspectorWidget

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 450)
        # setting status bar message
        self.statusBar().showMessage("Version: " + cs.VERSION_NUM_INSPECTOR)
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, cs.MAX_NUM_DETAILS)
        #self.progressBar.setFormat('Connected')
        #self.progressBar.setTextVisible(False)
        #self.progressBar.setValue(5)
        self.progressBar.setHidden(True)
        self.statusBar().addPermanentWidget(self.progressBar)

class Inspector(InspectorWidget):
    def __init__(self, window):
        super().__init__()
        self.parentWindow = window

    def inspectPushButtonClicked(self):
        print('inspectPushButtonClicked called')
        self.parentWindow.progressBar.setValue(0)
        
        fullName = self.idLineEdit.text().strip()
        self.work.plaerName = fullName
        
        if '#' in fullName:
            #检查名字是否过短
            if len(fullName) >= 5:
                self.work.start()
                self.textEdit.appendHtml(self.getHtml(fullName, 'OrangeRed'))
                self.parentWindow.progressBar.setHidden(False)
                return
        
        self.textEdit.appendHtml(self.getHtml(fullName + ' is invalid, please input name and tag seperated by # eg: storm#5961', 'OrangeRed')) 
        return super().inspectPushButtonClicked()

    def showFinish(self, text):
        self.parentWindow.progressBar.setHidden(True)
        return super().showFinish(text)

    def showlog(self, opponentName, outcome, deckCode, factions, opDeckCode, opFactions, totalTurn, num):
        self.parentWindow.progressBar.setValue(num)
        return super().showlog(opponentName, outcome, deckCode, factions, opDeckCode, opFactions, totalTurn, num)


app = QApplication(sys.argv)
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app.setApplicationName(cs.DISPLAY_TITLE)
app.setWindowIcon(QIcon('test.jpg'))
app.setStyle('Fusion')
window = Window()
inspectorWidget = Inspector(window)
window.setCentralWidget(inspectorWidget)
window.show()
sys.exit(app.exec())