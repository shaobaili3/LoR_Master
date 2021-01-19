from PyQt5.QtCore import QThread, pyqtSignal
from local import Local


class TrackThread(QThread):
    showMessage = pyqtSignal(str)
    showDecks = pyqtSignal(str, str)

    def __int__(self):
        super().__init__()
        self.local = None
        self.player = None

    def run(self):
        print('tracker running')
        while(True):
            self.local.updateStatus(self.player.checkOpponent)
            if not self.isRunning():
                return
        