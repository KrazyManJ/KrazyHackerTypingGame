import os
import random

import pygame
import pygame.freetype
from pygame import gfxdraw, mixer, Rect, freetype

pygame.init()
pygame.display.set_icon(pygame.image.load(os.path.join("src", "krazyhackertypinggame.png")))
pygame.display.set_caption("KrazyHackerTypingGame", os.path.join("src", "krazyhackertypinggame.png"))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if False else pygame.display.set_mode((1280, 720))

def __keyStructure(name,size,label,kmod=None,key=None,font="fira code") -> dict:
    d = {}
    d["name"] = name
    d["size"] = size
    d["label"] = label
    if None != kmod: d["mod"] = kmod
    if None != key: d["key"] = key
    d["font"] = font
    return d

KEY_SIZE = screen.get_rect().width * 0.0455
KEY_THICK = KEY_SIZE // 20
KEY_GAP = KEY_SIZE * 0.1
KEY_LABEL_SIZE = KEY_SIZE//2.5
KEYBOARD_KEYS = [
    list("`1234567890=´"),
    list("qwertyuiop[]"),
    list("asdfghjkl;'\\"),
    list("zxcvbnm,./"),
]
KEYBOARD = [
    [
        list("`1234567890=´"),
        __keyStructure("backspace",2,"←",key=pygame.K_BACKSPACE,font="cambria")
    ],
    [
        __keyStructure("tab",1.5,"⇄",key=pygame.K_TAB,font="cambria"),
        list("qwertyuiop[]"),
        "enter"
    ],
    [
        __keyStructure("caps",1.75,"CAPS",kmod=pygame.KMOD_CAPS),
        list("asdfghjkl;'\\")
    ],
    [
        __keyStructure("",2.25,"SHIFT",kmod=pygame.KMOD_LSHIFT),
        list("zxcvbnm,./"),
        __keyStructure("",2.8,"SHIFT",kmod=pygame.KMOD_RSHIFT),
    ],
    [
        __keyStructure("",1.5,"CTRL",kmod=pygame.KMOD_LCTRL),
        __keyStructure("",1.5,""),
        __keyStructure("",1.5,"ALT",kmod=pygame.KMOD_LALT),
        __keyStructure("space",6,"-"),
        __keyStructure("",1.25,"ALT",kmod=pygame.KMOD_RALT),
        __keyStructure("",1.25,""),
        __keyStructure("",1.25,""),
        __keyStructure("",1.35,"CTRL",kmod=pygame.KMOD_RCTRL)
    ]
]


class __C:
    white = (255, 255, 255)
    light_gray = (128, 128, 128)
    black = (0, 0, 0)
    green = (0, 255, 0)
    greenst = (0, 255, 0, 128)
    red = (255, 0, 0)
    gray = (0, 70, 0)

class __S:
    key = mixer.Sound(os.path.join("src", "sounds", "typing.mp3"))
    rowc = mixer.Sound(os.path.join("src", "sounds", "row_complete.wav"))
    lost = mixer.Sound(os.path.join("src", "sounds", "lost.wav"))

__codes = [
    "System.out.println('hello world!');",
    "#include <stdio.h>",
    "#include <iostream>",
    "from kernel import decrypter",
    "#define TCP_ACK 0x10;",
    "protect(-1,Hodor);"
]
__typed_text = ""
__chosencode = random.choice(__codes)

def __getPressedKeys():
    keys,tkey = pygame.key.get_pressed(),[]
    for key in range(len(keys)):
        if keys[key]:
            tkey.append(pygame.key.name(key))
    return tkey

def __rect(x, y, width, height, color, thickness, color2=__C.black) -> Rect:
    r1,r2 = Rect(x, y, width, height),Rect(x, y, width - thickness * 2, height - thickness * 2)
    r2.center = r1.center
    gfxdraw.box(screen, r1, color)
    gfxdraw.box(screen, r2, color2)
    return r2

def __centeredTextF(font, text, rect, color):
    ft = freetype.SysFont(font, KEY_LABEL_SIZE)
    r = ft.get_rect(text, size=KEY_LABEL_SIZE)
    r.center = rect.center
    ft.render_to(screen, r, text, color)

def __key(key, x, y, sx=KEY_SIZE, label=None, pr=None, font="fira code"):
    colors = [__C.green,__C.black] if __getPressedKeys().__contains__(key) or pr else [__C.black, __C.green]
    rect = __rect(x, y, sx, KEY_SIZE, colors[1], KEY_THICK, color2=colors[0])
    __centeredTextF(font, label if None != label else key.upper(), rect, colors[1])

def __enter(x, y):
    colors = [__C.green,__C.black] if __getPressedKeys().__contains__("return") else [__C.black,__C.green]
    rect = Rect(x,y,KEY_SIZE+KEY_GAP,KEY_SIZE*2+KEY_GAP)
    recti = Rect(x + KEY_THICK, y + KEY_THICK, rect.width - KEY_THICK * 2, rect.height - KEY_THICK * 2)
    rect2 = __rect(x, y, KEY_SIZE * 1.5, KEY_SIZE, colors[1], KEY_THICK, color2=colors[0])
    cord = list(rect2.topright)
    cord[0] = cord[0] + KEY_THICK
    cord[1] = cord[1] - KEY_THICK
    rect.topright = tuple(cord)
    recti.center = rect.center
    gfxdraw.box(screen,rect,colors[1])
    gfxdraw.box(screen,recti,colors[0])
    gfxdraw.box(screen,rect2,colors[0])
    __centeredTextF("cambria","⏎",rect,colors[1])

def mod(modd) -> bool:
    return False if None == modd else pygame.key.get_mods() & modd

def __keyboard(x, y):
    tx,ty = x,y
    for rows in KEYBOARD:
        for key in rows:
            if type(key) == list:
                for k in key:
                    __key(k,tx,ty)
                    tx += KEY_SIZE+KEY_GAP
                pass
            elif type(key) == dict:
                size = (key["size"]*KEY_SIZE)+((key["size"]-2)*KEY_GAP)
                if "mod" in key:
                    __key(key["name"],tx,ty,size,key["label"],font=key["font"],pr=mod(key["mod"]))
                elif "key" in key:
                    __key(key["name"],tx,ty,size,key["label"],font=key["font"],pr=pygame.key.get_pressed()[key["key"]])
                else:
                    __key(key["name"],tx,ty,size,key["label"],font=key["font"])
                tx += size+KEY_GAP
                pass
            elif key == "enter":
                __enter(tx,ty)
        tx = x
        ty += KEY_GAP+KEY_SIZE

def __keyboardSize():
    s = 0
    for i in range(len(KEYBOARD_KEYS)):
        if len(KEYBOARD_KEYS[i]) + (i / 2) > s:
            s = len(KEYBOARD_KEYS[i]) + (i / 2)
    x = (s + 3.6) * (KEY_SIZE+KEY_GAP) - KEY_SIZE*2
    y = len(KEYBOARD_KEYS) * (KEY_SIZE+KEY_GAP) + KEY_SIZE
    return x, y

def main():
    global __typed_text, __chosencode

    clock = pygame.time.Clock()

    kx = screen.get_rect().centerx - __keyboardSize()[0] / 2
    ky = screen.get_rect().centery - __keyboardSize()[1] / 2

    channelid = 0
    mixer.init()
    for i in range(8): mixer.Channel(i).set_volume(0.2)
    mixer.set_num_channels(9)

    run = True
    while run:
        clock.tick(60)
        screen.fill(__C.black)

        __keyboard(kx, ky * 1.7)
        __rect(kx, ky * 0.3, __keyboardSize()[0], __keyboardSize()[1] / 2, __C.green, KEY_THICK)

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
                    mixer.Channel(channelid).play(__S.key)
                    channelid += channelid * -1 if channelid >= 7 else 1
                    print(__typed_text)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__": main()
