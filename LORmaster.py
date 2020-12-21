from network import Network
from pystray import Icon as icon, Menu as menu, MenuItem as item
import sys
import time
import webbrowser
from io import BytesIO
from PIL import Image, ImageFile

from local import Local
from match import Match
from opponent import Opponent

# orig_stdout = sys.stdout
# f = open('history.log', 'a')
# sys.stdout = f
# print(time.localtime())
# #sys.stdout = orig_stdout
# #f.close()

local = Local()
network = Network()
match = Match(network)
check = Opponent(match)

ImageFile.LOAD_TRUNCATED_IMAGES = True

with open('Resource/image.png', 'rb') as f:
    b = BytesIO()
    b.write(f.read())
    image = Image.open(b)
    image.load()

def work(stray):
    stray.visible = True
    if stray.HAS_NOTIFICATION:
        stray.notify("对手套牌查询已启动", title="LOR大师") #LoR Master Tracker is running 
    while stray.visible:
        #print("xxxx")
        time.sleep(1)
        local.updateStatus(check.checkOpponent)
        #print(stray.visible)
    sys.exit()

def checkAgain(stray):
    check.showOpponentAgain()

def quitApp(stray):
    stray.visible = False
    stray.stop()
    sys.exit()
    return

def versionApp(stray):
    link = "https://github.com/shaobaili3/lor_master/releases"
    webbrowser.open(link)

state = 'americas'

def set_state(v):
    def inner():
        global state
        state = v
    return inner

def get_state(v):
    def inner(item):
        return state == v
    return inner

def show(v):
    return '服务器: ' + str(state)


itemCheckAgain = item('重新显示牌组', checkAgain) # Reopen latest decks
itemVersion = item('版本: 0.3.0内测', versionApp) #Check for update
itemQuit = item('退出', quitApp) # Quit



americasItem = item('americas (NA美服)',
        set_state('americas'),
        checked=get_state('americas'),
        radio=True)
europeItem = item('europe (EU欧服)',
        set_state('europe'),
        checked=get_state('europe'),
        radio=True)
asiaItem = item('asia (ASIA亚服)',
        set_state('asia'),
        checked=get_state('asia'),
        radio=True)


subMenu = item(show, menu(americasItem, europeItem, asiaItem))

menuWithItems = menu(itemCheckAgain, itemVersion, subMenu, itemQuit)

print(local)

icon('LOR Master Tracker', image, title = "LOR Master Tracker V0.3.0", menu=menuWithItems).run(work)