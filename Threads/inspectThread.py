from PyQt5.QtCore import QThread, pyqtSignal


class InspectThread(QThread):
    showLogtrigger = pyqtSignal(str, str, str, str, str, str, str, str, int)
    finishTrigger = pyqtSignal(str, str)
    summaryTigger = pyqtSignal(dict)

    def __int__(self):
        super().__init__()
        self.playerName = ''
        self.player = None

    def run(self):
        print('running')
        fullname = self.playerName.strip().split('#')
        try:
            self.player.inspectPlayer(fullname[0], fullname[1],
                                      self.showLogtrigger.emit,
                                      self.summaryTigger.emit,
                                      self.finishTrigger.emit)
        except IndexError:
            return
