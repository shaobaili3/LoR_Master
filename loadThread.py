from PyQt5.QtCore import QThread, pyqtSignal
class LoadThread(QThread):
    trigger = pyqtSignal(str, str, str)
    

    def __int__(self):
        super(LoadThread, self).__init__()
        self.plaerName = ''
        self.player = None
    
    def run(self):
        print('running')
        fullname = self.plaerName.strip().split('#')
        self.player.inspectPlayer(fullname[0], fullname[1], self.trigger.emit)

