from PySide6.QtCore import QThread, Signal


class InspectThread(QThread):
    showLogtrigger = Signal(str, str, str, str, str, str, str, int, int)
    finishTrigger = Signal(str, str)
    summaryTigger = Signal(dict)

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
