
from pystray import Icon as icon, Menu as menu, MenuItem as item
import sys
import time
import webbrowser
from io import BytesIO
from PIL import Image, ImageFile

from local import Local
from match import Match
from opponent import Opponent

local = Local()
check = Opponent()

state = False

ImageFile.LOAD_TRUNCATED_IMAGES = True

with open('image.png', 'rb') as f:
    b = BytesIO()
    b.write(f.read())

    image = Image.open(b)
    image.load()

def work(stray):
    stray.visible = True
    stray.notify("对手套牌查询已启动", title="LOR大师")
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


print(local)

icon('LOR Master Tracker', image, title = "LOR Master Tracker V0.22", menu=menuWithItems).run(work)



