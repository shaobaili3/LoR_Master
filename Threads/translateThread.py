from PyQt5.QtCore import QThread, pyqtSignal
from translate import detect


class TranslateThread(QThread):
    def __int__(self):
        super().__init__()

    def run(self):
        detect()
