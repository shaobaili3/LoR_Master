from PyQt5.QtCore import QThread, pyqtSignal

import time


class TrackThread(QThread):
    showDecksTrigger = pyqtSignal(dict, int)
    showStatusTrigger = pyqtSignal(str)
    showMatchsTrigger = pyqtSignal(str, str, str, str)
    showMessageTrigger = pyqtSignal(str)

    def __int__(self):
        super().__init__()
        self.local = None
        self.player = None

    def run(self):
        print('tracker running')
        while (True):
            time.sleep(1)
            # print('tracking detecting')
            self.local.updateStatus(self.player.checkOpponent,
                                    self.showMessageTrigger.emit,
                                    self.showStatusTrigger.emit,
                                    self.showMatchsTrigger.emit,
                                    self.showDecksTrigger.emit)
            if not self.isRunning():
                return
