import os
from PyQt5.QtCore import QThread
if os.name == 'nt':
    from translate import detect
else:

    def detect():
        print('translate in macOS')
        return


class TranslateThread(QThread):
    def __int__(self):
        super().__init__()

    def run(self):
        detect()
