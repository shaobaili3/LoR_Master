from PyQt5.QtCore import QThread, pyqtSignal
class LoadThread(QThread):
    trigger = pyqtSignal(str)
    def __int__(self):
        # 初始化函数
        super(LoadThread, self).__init__()

    def run(self):
        self.trigger.emit(str(10))