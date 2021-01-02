import os
import sys
import webbrowser
import constants as cs
from setting import Setting, Server
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore
from PyQt5 import QtGui

from local import Local
from match import Match
from network import Network
from opponent import Opponent

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(cs.DISPLAY_TITLE + ' v' + cs.VERSION_NUM)
        self.setWindowIcon(QIcon('test.jpg'))
        self.resize(840, 512)
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        styleComboBox = QComboBox()
        styleComboBox.addItems(list(map(str, Server)))
        styleLabel = QLabel("Server:")
        styleLabel.setBuddy(styleComboBox)
        idLabel = QLabel("Riot ID:")
        self.idLineEdit = QLineEdit(self)
        self.idLineEdit.textChanged.connect(self.idLineEditChanged)
        tagLabel = QLabel("#")
        self.tagLineEdit = QLineEdit(self)
        
        #self.tagLineEdit.setReadOnly(True)
        #self.tagLineEdit.textChanged.connect(self.tagLineEditChanged)

        defaultPushButton = QPushButton("Inspect")
        defaultPushButton.setDefault(True)
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)

        topLayout.addWidget(idLabel)
        topLayout.addWidget(self.idLineEdit)

        topLayout.addWidget(tagLabel)
        topLayout.addWidget(self.tagLineEdit)

        topLayout.addStretch(1)

        topLayout.addWidget(defaultPushButton)

        textLayout = QHBoxLayout()
        self.textEdit = QPlainTextEdit()
        self.textEdit.setReadOnly(True)
        textLayout.addWidget(self.textEdit)
        self.textEdit.appendPlainText("new content")
        self.textEdit.appendHtml(
            "<font color = \"IndianRed\"> Sample Text</font><font color = \"DarkOrange\"> Sample Text</font>")
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(textLayout)
        self.setLayout(outerLayout)
    
    def idLineEditChanged(self):
        print(self.idLineEdit.text().strip())
        tag = local.getTagByName(self.idLineEdit.text().strip())
        print(tag, '!!!!!!!!!!!!!!!!!')
        if tag is None:
            self.textEdit.appendPlainText('id: ' + self.idLineEdit.text().strip() +  '找不到tag, 请手动输入...')
        else:
            self.textEdit.appendPlainText('发现玩家:' + self.idLineEdit.text().strip() + '#' + tag + '正在查询对局信息...' )

    def tagLineEditChanged(self):
        print(self.tagLineEdit.text())
        pass


def addTray():
    tray.setIcon(QIcon('test.jpg'))
    showAction = QAction(cs.DISPLAY_TITLE + '大师', triggered=showTrigger)
    versionAction = QAction('版本: ' + cs.VERSION_NUM + '内测', triggered = versionTrigger)
    quitAction = QAction('退出', triggered=quitTrigger)
    tpMenu = QMenu()
    tpMenu.addAction(showAction)
    tpMenu.addAction(versionAction)
    tpMenu.addAction(quitAction)
    tray.setContextMenu(tpMenu)
    tray.setToolTip(cs.DISPLAY_TITLE)
    tray.show()
    tray.activated.connect(showTrigger)
    app_icon = QIcon('test.jpg')
    tray.showMessage(cs.DISPLAY_TITLE, "LoR大师已启动",app_icon)
    sys.exit(app.exec_())


def showTrigger():
    window.show()
    window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
    window.activateWindow()

def quitTrigger():
    QCoreApplication.instance().quit()
    tray.setVisible(False)

def versionTrigger():
    link = "https://github.com/shaobaili3/lor_master/releases"
    webbrowser.open(link)


setting = Setting()
setting.setServer(Server.NA)
network = Network(setting)
match = Match(network)
opponent = Opponent(match)
local = Local(setting)


os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
app.setApplicationName(cs.DISPLAY_TITLE + '#')
app.setWindowIcon(QIcon('test.jpg'))
window = Window()
window.show()
window.activateWindow()
tray = QSystemTrayIcon()
# 关闭所有窗口,也不关闭应用程序
app.setQuitOnLastWindowClosed(False)
addTray()
