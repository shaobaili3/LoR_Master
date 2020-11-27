from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageFile
from io import BytesIO

with open('image.png', 'rb') as f:
    b = BytesIO()
    b.write(f.read())

    image = Image.open(b)
    image.load()


icon('test', image, menu=menu(
    item(
        'With submenu',
        menu(
            item(
                'Show message',
                lambda icon, item: icon.notify('Hello World!')),
            item(
                'Submenu item 2',
                lambda icon, item: icon.remove_notification()))))).run()