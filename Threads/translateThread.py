import os
import time
from PyQt5.QtCore import QThread
if os.name == 'nt':
    from Models.translate import detect
else:
    def detect():
        print('translate in macOS')
        while True:
            time.sleep(999999)
        return


class TranslateThread(QThread):
    def __int__(self):
        super().__init__()

    def run(self):
        detect()
