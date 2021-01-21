from PyQt5.QtCore import QThread, pyqtSignal
from local import Local
import time


class TrackThread(QThread):
    #showMessage = pyqtSignal(str)
    showDecksTrigger = pyqtSignal(dict)
    showStatusTrigger = pyqtSignal(str)

    def __int__(self):
        super().__init__()
        self.local = None
        self.player = None

    def run(self):
        print('tracker running')
        while(True):
            time.sleep(1)
            # print('tracking detecting')
            self.local.updateStatus(self.player.checkOpponent, self.showStatusTrigger.emit, self.showDecksTrigger.emit)
            if not self.isRunning():
                return
