from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageFile
from io import BytesIO

with open('Resource/image.png', 'rb') as f:
    b = BytesIO()
    b.write(f.read())

    image = Image.open(b)
    image.load()


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

# Let the menu items be a callable returning a sequence of menu
# items to allow the menu to grow

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

menuWithItems = menu(subMenu)

icon('LOR Master Tracker', image, title = "LOR Master Tracker V0.2.3", menu=menuWithItems).run()


#asia europe americas