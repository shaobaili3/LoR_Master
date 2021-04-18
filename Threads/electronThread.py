import Models.process
from PyQt5.QtCore import QThread

class ElectronThread(QThread):
    def __int__(self):
        super().__init__()

    def run(self):
        Models.process.runElectron()
