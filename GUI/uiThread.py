from PyQt5.QtCore import QThread, pyqtSignal
#from process import updateTrackServer
import zerorpc



class UIThread(QThread):

    def __int__(self):
        super().__init__()
        self.ui = None

    def run(self):
        pass
        s = zerorpc.Server(self.ui)
        s.bind("tcp://0.0.0.0:6393")
        s.run()

