from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication([])
#app.setQuitOnLastWindowClosed(False)

# # Create the tray
# tray = QSystemTrayIcon()
# tray.setIcon(icon)
# tray.setVisible(True)

# # Create the menu
# menu = QMenu()
# action = QAction("A menu item")
# menu.addAction(action)

# # Add a Quit option to the menu.
# quit = QAction("Quit")
# quit.triggered.connect(app.quit)
# menu.addAction(quit)

# # Add the menu to the tray
# tray.setContextMenu(menu)


tray = QSystemTrayIcon()
tray.setIcon(QIcon('test.jpg'))
# 设置系统托盘图标的菜单
a1 = QAction('显示(Show)')
tpMenu = QMenu()
tpMenu.addAction(a1)
#tpMenu.addAction(a2)
#tpMenu.addAction(a3)
tray.setContextMenu(tpMenu)
tray.show()
app.exec_()