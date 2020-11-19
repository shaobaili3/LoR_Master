from PIL import Image
from pystray import Icon as icon, Menu as menu, MenuItem as item
import sys
import time
import webbrowser


from local import Local
from match import Match
from opponent import Opponent


local = Local()
check = Opponent()



state = False
image = Image.open("icon.ico")


def work(stray):
    stray.visible = True
    while stray.visible:
        #print("xxxx")
        time.sleep(1)
        local.updateStatus(check.checkOpponent)
        print(stray.visible)
    sys.exit()


def checkAgain(stray):
    check.showOpponentAgain()
    #stray.update_menu
    #stray.visible = True

def quitApp(stray):
    print("hehe")
    state = True
    stray.visible = False
    stray.stop()
    sys.exit()
    return

def versionApp(stray):
    link = "https://github.com/shaobaili3/lor_master/releases"
    webbrowser.open(link)


itemCheckAgain = item('重新显示牌组', checkAgain)
itemVersion = item('版本V0.2测试版', versionApp)
itemQuit = item('退出', quitApp)

menuWithItems = menu(itemCheckAgain, itemVersion, itemQuit)
icon('LOR Master Tracker', image, title = "LOR Master Tracker V0.2", menu=menuWithItems).run(work)

