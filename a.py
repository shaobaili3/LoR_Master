import sys
import webbrowser
import constants as cs
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LoR Master Tracker")
        self.resize(600, 480)
        outerLayout = QVBoxLayout()
        topLayout = QHBoxLayout()
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())
        styleLabel = QLabel("Server:")
        styleLabel.setBuddy(styleComboBox)
        idLabel = QLabel("Riot ID:")
        idLineEdit = QLineEdit('')
        #idLineEdit.placeholderText = 'id'
        tagLabel = QLabel("#")
        tagLineEdit = QLineEdit('')

        defaultPushButton = QPushButton("Inspect")
        defaultPushButton.setDefault(True)
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)

        topLayout.addWidget(idLabel)
        topLayout.addWidget(idLineEdit)

        topLayout.addWidget(tagLabel)
        topLayout.addWidget(tagLineEdit)

        tagLineEdit.setEnabled = False
        topLayout.addStretch(1)

        topLayout.addWidget(defaultPushButton)

        textLayout = QHBoxLayout()
        textEdit = QPlainTextEdit()
        textEdit.setReadOnly(True)
        textLayout.addWidget(textEdit)
        textEdit.appendPlainText("new content")
        textEdit.appendPlainText("new content2222")
        textEdit.appendHtml(
            "<font color = \"IndianRed\"> Sample Text</font><font color = \"DarkOrange\"> Sample Text</font>")
        # Nest the inner layouts into the outer layout
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(textLayout)
        # Set the window's main layout
        self.setLayout(outerLayout)
        # self.app.exec_()


def addTray():
    
    # window.show()
    tray.setIcon(QIcon('test.jpg'))
    #
    # 设置系统托盘图标的菜单
    showAction = QAction(cs.DISPLAY_TITLE + '大师', triggered=showTrigger)
    versionAction = QAction('版本: ' + cs.VERSION_NUM + '内测', triggered = versionTrigger)
    quitAction = QAction('退出', triggered=quitTrigger)
    tpMenu = QMenu()
    tpMenu.addAction(showAction)
    tpMenu.addAction(versionAction)
    tpMenu.addAction(quitAction)
    tray.setContextMenu(tpMenu)
    tray.show()
    sys.exit(app.exec_())


def showTrigger():
    print("showTrigger")
    # this will remove minimized status 
    # and restore window with keeping maximized/normal state
    window.show()
    window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
    # this will activate the window
    window.activateWindow()
    #window.setWindowFlags(QtCore.Qt.Widget) #取消置顶
    
    

def quitTrigger():
    QCoreApplication.instance().quit()
    tray.setVisible(False)

def versionTrigger(stray):
    link = "https://github.com/shaobaili3/lor_master/releases"
    webbrowser.open(link)


app = QApplication(sys.argv)
window = Window()
window.show()

tray = QSystemTrayIcon()
# 关闭所有窗口,也不关闭应用程序
app.setQuitOnLastWindowClosed(False)


addTray()
