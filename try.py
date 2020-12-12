from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageFile
from io import BytesIO

with open('Resource/image.png', 'rb') as f:
    b = BytesIO()
    b.write(f.read())

    image = Image.open(b)
    image.load()


state = 0

def set_state(v):
    def inner(icon, item):
        global state
        state = v
    return inner

def get_state(v):
    def inner(item):
        return state == v
    return inner

# Let the menu items be a callable returning a sequence of menu
# items to allow the menu to grow
icon('test', image, menu=menu(lambda: (
    item(
        'State %d' % i,
        set_state(i),
        checked=get_state(i),
        radio=True)
    for i in range(max(2, state + 2))))).run()