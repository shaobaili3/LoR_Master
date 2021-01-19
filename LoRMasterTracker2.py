import sys
import time
import webbrowser
from asyncio.windows_events import NULL
from io import BytesIO

from PIL import Image, ImageFile
from pystray import Icon as icon
from pystray import Menu as menu
from pystray import MenuItem as item

import constants as cs
from local import Local
from riot import Riot
from network import Network
from player import Player
from setting import Server, Setting

# orig_stdout = sys.stdout
# f = open('history.log', 'a')
# sys.stdout = f
# print(time.localtime())
# #sys.stdout = orig_stdout
# #f.close()

setting = Setting()
network = Network(setting)
riot = Riot(network)
opponent = Player(riot)
state = setting.getServer()
local = NULL

# opponent.checkOpponent('Storm', '5961')
ImageFile.LOAD_TRUNCATED_IMAGES = True
with open('Resource/image.png', 'rb') as f:
    b = BytesIO()
    b.write(f.read())
    image = Image.open(b)
    image.load()


def work(stray):
    stray.visible = True
    global local
    local = Local(setting)
    if stray.HAS_NOTIFICATION:
        # LoR Master Tracker is running
        stray.notify("对手套牌查询已启动", title=cs.DISPLAY_TITLE)
    while stray.visible:
        # print("xxxx")
        time.sleep(1)
        local.updateStatus(opponent.checkOpponent)
        # print(stray.visible)


def checkAgain(stray):
    opponent.showOpponentAgain()


def quitApp(stray):
    stray.visible = False
    stray.stop()
    sys.exit()


def versionApp(stray):
    link = "https://github.com/shaobaili3/lor_master/releases"
    webbrowser.open(link)


def set_state(server):
    def inner():
        setting.setServer(server)
        local.reset()
        global state
        state = server.value
    return inner


def get_state(v):
    def inner(item):
        return state == v
    return inner


def show(v):
    return '服务器: ' + str(state)


itemCheckAgain = item('重新显示牌组', checkAgain)  # Reopen latest decks
itemVersion = item('版本: ' + cs.VERSION_NUM + '内测', versionApp)  # Check for update
itemQuit = item('退出', quitApp)  # Quit

americasItem = item('americas (NA美服)', set_state(Server.NA), checked=get_state('americas'), radio=True)
europeItem = item('europe (EU欧服)', set_state(Server.EU), checked=get_state('europe'), radio=True)
asiaItem = item('asia (ASIA亚服)', set_state(Server.ASIA), checked=get_state('asia'), radio=True)

subMenu = item(show, menu(americasItem, europeItem, asiaItem))

menuWithItems = menu(itemCheckAgain, itemVersion, subMenu, itemQuit)

icon('LOR Master Tracker', image, title="LOR Master Tracker v" + cs.VERSION_NUM, menu=menuWithItems).run(work)
