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
        self.resize(800, 500)
        # setting status bar message
        self.statusBar().showMessage("Version: 0.1.0 beta")
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 5)
        self.progressBar.setFormat('Connected')
        #self.progressBar.setTextVisible(False)
        self.progressBar.setValue(5)
        self.progressBar.text
        self.statusBar().addPermanentWidget(self.progressBar)


class Inspector(InspectorWidget):
    def __init__(self, window):
        super().__init__()
        self.parentWindow = window

    def showlog(self, opponentName, outcome, deckCode):
        super().showlog(opponentName=opponentName, outcome=outcome, deckCode=deckCode)
        window.progressBar.setFormat(deckCode)
        print('InspectorWidget son called')

app = QApplication(sys.argv)
#window.setCentralWidget = 
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app.setApplicationName(cs.DISPLAY_TITLE)
app.setWindowIcon(QIcon('test.jpg'))
app.setStyle('Fusion')
window = Window()
inspectorWidget = Inspector(window)
window.setCentralWidget(inspectorWidget)
window.show()
sys.exit(app.exec())
