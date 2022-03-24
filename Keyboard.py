import pygame
from pygame import gfxdraw, Rect
from typing import Final
import GraphUtils
import Color


def __a(name, keysize, label, key=None, font="fira code") -> dict:
    return {"name": name, "size": keysize, "label": label, "font": font, "key": key}


KEY_SIZE: int
KEY_THICK: int
KEY_GAP: int
KEY_LABEL_SIZE: int
LAYOUT: Final = [
    [list("`1234567890=´"), __a("backspace", 2, "←", key=pygame.K_BACKSPACE, font="cambria")],
    [__a("tab", 1.5, "⇄", font="cambria"), list("qwertyuiop[]"), "enter"],
    [__a("caps", 1.75, "CAPS", key=pygame.KMOD_CAPS), list("asdfghjkl;'\\")],
    [__a("", 2.25, "SHIFT", key=pygame.KMOD_LSHIFT), list("zxcvbnm,./"),
     __a("", 2.75, "SHIFT", key=pygame.KMOD_RSHIFT), ],
    [
        __a("", 1.3, "CTRL", key=pygame.KMOD_LCTRL), __a("", 1.3, ""), __a("", 1.3, "ALT", key=pygame.KMOD_LALT),
        __a("space", 5.75, "-"),
        __a("", 1.25, "ALT", key=pygame.KMOD_RALT), __a("", 1.25, ""), __a("", 1.25, ""),
        __a("", 1.6, "CTRL", key=pygame.KMOD_RCTRL)
    ]
]


def init(keysize):
    global KEY_SIZE, KEY_THICK, KEY_GAP, KEY_LABEL_SIZE
    KEY_SIZE = keysize
    KEY_THICK = KEY_SIZE // 20
    KEY_GAP = KEY_SIZE // 10
    KEY_LABEL_SIZE = KEY_SIZE // 2.5
    is_initialized()


def is_initialized():
    if KEY_SIZE <= 0:
        raise ValueError("Keyboard is not initialized properly! Initialize it with positive number first!")


def draw(surface, x: int, y: int, color: tuple[int, int, int]):
    is_initialized()
    tx = x
    for rows in LAYOUT:
        for key in rows:
            if type(key) == list:
                for k in key:
                    __key(surface, k, tx, y, color, KEY_SIZE)
                    tx += KEY_SIZE + KEY_GAP
            elif type(key) == dict:
                s = key["size"] * KEY_SIZE + (key["size"] - 1) * KEY_GAP
                __key(surface, key["name"], tx, y, color, s, label=key["label"], font=key["font"],
                      pr=__pressed(key["key"]))
                tx += s + KEY_GAP
            elif key == "enter":
                __enter(surface, tx, y, color)
        tx = x
        y += KEY_GAP + KEY_SIZE


def size() -> tuple[float, float]:
    s = 0
    for i in range(len(LAYOUT)):
        s = rowsize(i) if rowsize(i) > s else s
    x = s + KEY_GAP
    y = len(LAYOUT) * KEY_SIZE + ((len(LAYOUT) - 1) * KEY_GAP)
    return x, y


def rowsize(index) -> float:
    t = 0
    for key in LAYOUT[index]:
        if type(key) is list:
            t += len(key) * KEY_SIZE + (len(key) - 1) * KEY_GAP
        elif type(key) is dict:
            t += key["size"] * KEY_SIZE + (key["size"] - 1) * KEY_GAP
    return t


def __getpressedkeys():
    keys, tkey = pygame.key.get_pressed(), []
    for key in range(len(keys)):
        if keys[key]:
            tkey.append(pygame.key.name(key))
    return tkey


def __key(surface, key, x, y, color, sx, label=None, pr=None, font="fira code"):
    rect = GraphUtils.draw_rect(surface, x, y, sx, KEY_SIZE, color, KEY_THICK,
                                invert=__getpressedkeys().__contains__(key) or pr)
    GraphUtils.draw_text_f(surface, font, label if label is not None else key.upper(),
                           KEY_LABEL_SIZE, rect,
                           Color.black if __getpressedkeys().__contains__(key) or pr else color)


def __enter(surface, x, y, color):
    width = 1.5

    colors = [color, Color.black] if __getpressedkeys().__contains__("return") else [Color.black, color]
    lowerwidth = size()[0] - rowsize(2) - KEY_GAP * 2

    rect = Rect(x, y, lowerwidth, KEY_SIZE * 2 + KEY_GAP)
    recti = Rect(x + KEY_THICK, y + KEY_THICK, rect.width - KEY_THICK * 2,
                 rect.height - KEY_THICK * 2)
    rect2 = GraphUtils.draw_rect(surface, x, y, width * KEY_SIZE + (width - 1) * KEY_GAP,
                                 KEY_SIZE, colors[1], KEY_THICK)
    cord = list(rect2.topright)
    cord[0] = cord[0] + KEY_THICK
    cord[1] = cord[1] - KEY_THICK
    rect.topright = tuple(cord)
    recti.center = rect.center
    gfxdraw.box(surface, rect, colors[1])
    gfxdraw.box(surface, recti, colors[0])
    gfxdraw.box(surface, rect2, colors[0])
    GraphUtils.draw_text_f(surface, "cambria", "⏎", KEY_LABEL_SIZE, rect, colors[1])


def __pressed(modd) -> bool:
    if type(modd) is None:
        return False
    elif type(modd) == int:
        return pygame.key.get_mods() & modd
    else:
        return __getpressedkeys().__contains__(modd)
