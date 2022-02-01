import os
import pygame
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def is_in(cords, rect_cords):
    x1, y1 = cords
    x2, y2, w, h = rect_cords
    return x2 <= x1 <= x2 + w and y2 <= y1 <= y2 + h
