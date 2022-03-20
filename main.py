import os
import random

import pygame
import pygame.freetype
from pygame import gfxdraw, mixer, Rect, freetype

pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join("src", "krazyhackertypinggame.png")))
pygame.display.set_caption("KrazyHackerTypingGame", os.path.join("src", "krazyhackertypinggame.png"))
__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if False else pygame.display.set_mode((1280, 720))

class __Color:
    white = (255, 255, 255)
    light_gray = (128, 128, 128)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    gray = (0, 70, 0)

class __Sound:
    key = mixer.Sound(os.path.join("src", "sounds", "typing.mp3"))
    rowc = mixer.Sound(os.path.join("src", "sounds", "row_complete.wav"))
    lost = mixer.Sound(os.path.join("src", "sounds", "lost.wav"))

__typed_text = ""

def __rect(x, y, width, height, color, thickness, color2=__Color.black) -> Rect:
    r1,r2 = Rect(x, y, width, height),Rect(x, y, width - thickness * 2, height - thickness * 2)
    r2.center = r1.center
    gfxdraw.box(__screen, r1, color)
    gfxdraw.box(__screen, r2, color2)
    return r2

def __centeredTextF(font, text, rect, color):
    ft = freetype.SysFont(font, __KEY_LABEL_SIZE)
    r = ft.get_rect(text, size=__KEY_LABEL_SIZE)
    r.center = rect.center
    ft.render_to(__screen, r, text, color)

def __keyR(name, size, label, key=None, font="fira code") -> dict:
    d = {}
    d["name"],d["size"],d["label"],d["font"],d["key"] = name,size,label,font,key
    return d

__KEY_SIZE = __screen.get_rect().width * 0.0455
__KEY_THICK = __KEY_SIZE // 20
__KEY_GAP = __KEY_SIZE * 0.1
__KEY_LABEL_SIZE = __KEY_SIZE // 2.5
__LAYOUT = [
    [list("`1234567890=´"), __keyR("backspace", 2, "←", key=pygame.K_BACKSPACE, font="cambria")],
    [__keyR("tab", 1.5, "⇄", font="cambria"), list("qwertyuiop[]"), "enter"],
    [__keyR("caps", 1.75, "CAPS", key=pygame.KMOD_CAPS), list("asdfghjkl;'\\")],
    [
        __keyR("", 2.25, "SHIFT", key=pygame.KMOD_LSHIFT),list("zxcvbnm,./"),
        __keyR("", 2.75, "SHIFT", key=pygame.KMOD_RSHIFT),
    ],
    [
        __keyR("", 1.3, "CTRL", key=pygame.KMOD_LCTRL),__keyR("", 1.3, ""),
        __keyR("", 1.3, "ALT", key=pygame.KMOD_LALT),__keyR("space", 5.75, "-"),
        __keyR("", 1.25, "ALT", key=pygame.KMOD_RALT),__keyR("", 1.25, ""),
        __keyR("", 1.25, ""),__keyR("", 1.6, "CTRL", key=pygame.KMOD_RCTRL)
    ]
]


def __getPressedKeys():
    keys,tkey = pygame.key.get_pressed(),[]
    for key in range(len(keys)):
        if keys[key]: tkey.append(pygame.key.name(key))
    return tkey

def __key(key, x, y, sx=__KEY_SIZE, label=None, pr=None, font="fira code"):
    colors = [__Color.green, __Color.black] if __getPressedKeys().__contains__(key) or pr else [__Color.black, __Color.green]
    rect = __rect(x, y, sx, __KEY_SIZE, colors[1], __KEY_THICK, color2=colors[0])
    __centeredTextF(font, label if None != label else key.upper(), rect, colors[1])

def __enter(x, y):
    width = 1.5

    colors = [__Color.green, __Color.black] if __getPressedKeys().__contains__("return") else [__Color.black, __Color.green]
    t = 0
    for key in __LAYOUT[2]:
        if type(key) is list: t += len(key) * __KEY_SIZE + (len(key) - 1) * __KEY_GAP
        elif type(key) is dict: t += key["size"] * __KEY_SIZE + (key["size"] - 1) * __KEY_GAP
    lowerwidth = __keyboardSize()[0] - t - __KEY_GAP * 2

    rect = Rect(x, y, lowerwidth, __KEY_SIZE * 2 + __KEY_GAP)
    recti = Rect(x + __KEY_THICK, y + __KEY_THICK, rect.width - __KEY_THICK * 2, rect.height - __KEY_THICK * 2)
    rect2 = __rect(x, y, width * __KEY_SIZE + (width - 1) * __KEY_GAP, __KEY_SIZE, colors[1], __KEY_THICK, color2=colors[0])
    cord = list(rect2.topright)
    cord[0] = cord[0] + __KEY_THICK
    cord[1] = cord[1] - __KEY_THICK
    rect.topright = tuple(cord)
    recti.center = rect.center
    gfxdraw.box(__screen, rect, colors[1])
    gfxdraw.box(__screen, recti, colors[0])
    gfxdraw.box(__screen, rect2, colors[0])
    __centeredTextF("cambria","⏎",rect,colors[1])

def __pressed(modd) -> bool:
    if type(modd) is None: return False
    elif type(modd) == int: return pygame.key.get_mods() & modd
    else: return __getPressedKeys().__contains__(modd)

def __keyboard(x, y):
    tx,ty = x,y
    for rows in __LAYOUT:
        for key in rows:
            if type(key) == list:
                for k in key:
                    __key(k,tx,ty)
                    tx += __KEY_SIZE + __KEY_GAP
            elif type(key) == dict:
                size = key["size"] * __KEY_SIZE + (key["size"] - 1) * __KEY_GAP
                __key(key["name"], tx, ty, size, key["label"], font=key["font"], pr=__pressed(key["key"]))
                tx += size + __KEY_GAP
            elif key == "enter":
                __enter(tx,ty)
        tx = x
        ty += __KEY_GAP + __KEY_SIZE

def __keyboardSize() -> tuple[float, float]:
    s=0
    for i in range(len(__LAYOUT)): s = __keyboardRowSize(i) if __keyboardRowSize(i) > s else s
    x = s + __KEY_GAP
    y = len(__LAYOUT) * __KEY_SIZE + ((len(__LAYOUT) - 1) * __KEY_GAP)
    return x, y

def __keyboardRowSize(index) -> float:
    t = 0
    for key in __LAYOUT[index]:
        if type(key) is list: t += len(key) * __KEY_SIZE + (len(key) - 1) * __KEY_GAP
        elif type(key) is dict: t += key["size"] * __KEY_SIZE + (key["size"] - 1) * __KEY_GAP
    return t

def main():
    global __typed_text

    clock = pygame.time.Clock()

    kx = __screen.get_rect().centerx - __keyboardSize()[0] / 2
    ky = __screen.get_rect().centery - __keyboardSize()[1] / 2

    channelid = 0
    mixer.init()
    for i in range(8): mixer.Channel(i).set_volume(0.2)
    mixer.set_num_channels(9)

    run = True
    while run:
        clock.tick(60)
        __screen.fill(__Color.black)

        __keyboard(kx, ky * 1.7)
        __rect(kx, ky * 0.3, __keyboardSize()[0], __keyboardSize()[1] / 2, __Color.green, __KEY_THICK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                ln = len(__typed_text)
                match event.key:
                    case pygame.K_ESCAPE:
                        run = False
                    case pygame.K_BACKSPACE:
                        __typed_text = __typed_text[:-1]
                    # case pygame.K_RETURN:
                    #     if __typed_text == __chosencode:
                    #         mixer.Channel(8).play(__S.rowc)
                    #         __typed_text = ""
                    #         __chosencode = random.choice(__codes)
                    #     else:
                    #         mixer.Channel(8).set_volume(0.2)
                    #         mixer.Channel(8).play(__S.lost)
                    #         clock.tick(1)
                    #         run = False
                    case pygame.K_DELETE:
                        pass
                    case _:
                        if len(event.unicode) > 0 and ord(event.unicode) > 31: __typed_text += event.unicode
                if len(__typed_text) != ln:
                    mixer.Channel(channelid).play(__Sound.key)
                    mixer.Channel(channelid).set_volume(random.uniform(0.1,0.2))
                    channelid += channelid * -1 if channelid >= 7 else 1

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__": main()
