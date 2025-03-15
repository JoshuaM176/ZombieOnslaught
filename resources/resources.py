import pygame as pg
from os import path, curdir

ROOT = path.abspath(curdir)

def load_sprite(name: str, category: str, colorkey=None, scale=8):
    fullname = path.join(ROOT, 'resources', 'textures', category, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()