import os
from PyQt5.QtCore import QThread, pyqtSignal
if os.name == 'nt':
    import translate
else:
    def detect():
        print('translate in macOS')
        return

class TranslateThread(QThread):
    def __int__(self):
        super().__init__()

    def run(self):
        detect()
