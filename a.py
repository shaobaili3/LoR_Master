from PIL import Image
import sys
import time
import webbrowser
from infi.systray import SysTrayIcon

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


# itemCheckAgain = item('重新显示牌组', checkAgain)
# itemVersion = item('版本V0.2测试版', versionApp)
# itemQuit = item('退出', quitApp)

# menuWithItems = menu(itemCheckAgain, itemVersion, itemQuit)
# icon('LOR Master Tracker', image, title = "LOR Master Tracker V0.2", menu=menuWithItems).run(work)


from infi.systray import SysTrayIcon
hover_text = "SysTrayIcon Demo"
def hello(sysTrayIcon):
    print("Hello World.")
def simon(sysTrayIcon):
    print ("Hello Simon.")
def bye(sysTrayIcon):
    print ('Bye, then.')
def do_nothing(sysTrayIcon):
    pass
menu_options = (('Say Hello', "hello.ico", hello),
                ('Do nothing', None, do_nothing),
                ('A sub-menu', "submenu.ico", (('Say Hello to Simon', "simon.ico", simon),
                                               ('Do nothing', None, do_nothing),
                                              ))
               )
sysTrayIcon = SysTrayIcon("main.ico", hover_text, menu_options, on_quit=bye, default_menu_index=1)
sysTrayIcon.start()