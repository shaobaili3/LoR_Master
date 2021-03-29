from PySide6.QtCore import QThread, Signal
from Models.leaderboard import updateLeaderboard
import time


class TrackThread(QThread):
    showDecksTrigger = Signal(dict, int)
    showStatusTrigger = Signal(str)
    showMatchsTrigger = Signal(str, str, str, str)
    showMessageTrigger = Signal(str)

    def __int__(self):
        super().__init__()
        self.local = None
        self.player = None

    def run(self):
        print('tracker running')
        updateLeaderboard()
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
