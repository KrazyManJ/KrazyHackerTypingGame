import os
import random

import pygame
import pygame.freetype
from pygame import gfxdraw, mixer

pygame.init()

FULLSCREEN = False


pygame.display.set_icon(pygame.image.load(os.path.join("src","krazyhackertypinggame.png")))
pygame.display.set_caption("KrazyHackerTypingGame",os.path.join("src","krazyhackertypinggame.png"))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if FULLSCREEN else pygame.display.set_mode((1280, 720))


class Color:
    black = (0, 0, 0)
    green = (0, 255, 0)
    greenst = (0, 255, 0, 128)
    red = (255, 0, 0)
    gray = (70,70,70)


class Sound:
    key = pygame.mixer.Sound(os.path.join("src", "sounds", "typing.mp3"))
    rowc = pygame.mixer.Sound(os.path.join("src", "sounds", "row_complete.wav"))
    lost = pygame.mixer.Sound(os.path.join("src","sounds","lost.wav"))


__keyboardKeys = [
    list("`1234567890=´"),
    list("qwertyuiop[]"),
    list("asdfghjkl;'\\"),
    list("zxcvbnm,./"),
    list()
]


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
    keys = pygame.key.get_pressed()
    tkey = []
    for key in range(len(keys)):
        if keys[key]:
            tkey.append(pygame.key.name(key))
    return tkey


def __key(key: str, x, y, size, sizex: int | None = None, label: str | None = None, predicate=None,inactive=False,font='fira code'):
    margin = size / 20
    pressedkeys = __getPressedKeys()
    if None == sizex: sizex = size
    rect = pygame.Rect(x, y, sizex, size)
    color1 = Color.green if pressedkeys.__contains__(key) or predicate else Color.black
    color2 = Color.black if pressedkeys.__contains__(key) or predicate else Color.green
    gfxdraw.box(screen, rect, color2 if not inactive else Color.gray)
    gfxdraw.box(screen, pygame.Rect(x + margin, y + margin, sizex - margin * 2, size - margin * 2), color1 if not inactive else Color.black)
    t = pygame.freetype.SysFont(font, round(size / 2))
    f = t.get_rect(label if None != label else key.upper(), size=size / 2)
    f.center = rect.center
    t.render_to(screen, f, label if None != label else key.upper(), color2)


def __enter(x, y, keysize):
    margin = keysize / 20
    pressedkeys = __getPressedKeys()
    box4 = pygame.Rect(x + margin + keysize / 2, y + margin, keysize * 1.1 - margin * 2,
                       keysize * 2 * 1.05 - margin * 2)
    color1 = Color.green if pressedkeys.__contains__("return") else Color.black
    color2 = Color.black if pressedkeys.__contains__("return") else Color.green
    gfxdraw.box(screen, pygame.Rect(x, y, keysize * 1.5 * 1.06, keysize), color2)
    gfxdraw.box(screen, pygame.Rect(x + keysize / 2, y, keysize * 1.1, keysize * 2 * 1.05), color2)
    gfxdraw.box(screen, pygame.Rect(x + margin, y + margin, keysize * 1.5 * 1.07 - margin * 2, keysize - margin * 2),
                color1)
    gfxdraw.box(screen, box4, color1)

    t = pygame.freetype.SysFont("cambria", round(keysize / 2))
    f = t.get_rect("⏎", size=keysize / 2)
    f.center = box4.center
    t.render_to(screen, f, "⏎", color2)


def __keyboard(x, y, keysize):
    tx = x
    ty = y
    for keyrow in __keyboardKeys:
        for i in range(len(keyrow)):
            __key(keyrow[i], tx + (keysize * 1.1 if __keyboardKeys.index(keyrow) != 0 else 0) + (keysize * 1.1) * i, ty,
                  keysize)
        match __keyboardKeys.index(keyrow):
            case 0:
                __key("backspace",
                      tx + (keysize * 1.1 if __keyboardKeys.index(keyrow) != 0 else 0) + (keysize * 1.1) * len(keyrow), ty,
                      keysize,
                      sizex=keysize * 2 * 1.05, label="←", font="cambria")
            case 1:
                __key("tab", x, ty, keysize, sizex=keysize * 1.5, label="⇄",font="cambria")
                __enter(tx + (keysize * (len(keyrow) + 1) + (keysize * 0.1 * (len(keyrow) + 1))), ty, keysize)
            case 2:
                __key("capslock", x, ty, keysize, sizex=keysize * 2, label="Caps",
                      predicate=(pygame.key.get_mods() & pygame.KMOD_CAPS))
            case 3:
                __key("shift",x,ty,keysize,sizex=keysize*2.5,label="Shift",
                      predicate=(pygame.key.get_mods() & pygame.KMOD_LSHIFT))
                __key("shift", tx+(keysize* (len(keyrow) + 1) + (keysize * 0.1 * (len(keyrow) + 1))), ty, keysize, sizex=keysize * 2.8, label="Shift",
                      predicate=(pygame.key.get_mods() & pygame.KMOD_RSHIFT))
            case 4:
                __key("control",x,ty,keysize,sizex=keysize*1.5,label="CTRL",
                      predicate=(pygame.key.get_mods() & pygame.KMOD_LCTRL))
                __key("", x+(keysize*1.6), ty, keysize, sizex=keysize * 1.2,inactive=True)
                __key("alt", x+(keysize*3)-(keysize*0.1), ty, keysize, sizex=keysize * 1.5, label="Alt",
                      predicate=(pygame.key.get_mods() & pygame.KMOD_LALT))
                __key("space", x + (keysize * 4.5), ty, keysize, sizex=keysize * 6, label="-")
                __key("", x + (keysize * 10.6), ty, keysize, sizex=keysize*1.5, label="ALT",
                      predicate=(pygame.key.get_mods() & pygame.KMOD_RALT))
                __key("", x + (keysize * 12.2), ty, keysize, sizex=keysize * 1.2, inactive=True)
                __key("", x + (keysize * 13.5), ty, keysize, sizex=keysize * 1.2, inactive=True)
                __key("control", x+(keysize*14.8), ty, keysize, sizex=keysize * 1.6, label="CTRL",
                      predicate=(pygame.key.get_mods() & pygame.KMOD_RCTRL))
        tx += keysize / 2
        ty += keysize * 1.1


def __keyboardSize(keysize):
    s = 0
    for i in range(len(__keyboardKeys)):
        if len(__keyboardKeys[i]) + (i / 2) > s:
            s = len(__keyboardKeys[i]) + (i / 2)
    x = (s + 2) * (keysize * 1.1) - (keysize * 0.2)
    y = len(__keyboardKeys) * (keysize * 1.1) - (keysize * 0.2)
    return x, y


def __text(x,y,size,text,color,opacity=255):
    font = pygame.font.SysFont("fira code", size // 2)
    text = font.render(text,True,color)
    text.set_alpha(opacity)
    textR = text.get_rect()
    textR.x = x
    textR.y = y
    screen.blit(text,textR)


def __textScreen(size):
    margin = size / 20
    keyboard_width = __keyboardSize(size)[0]
    rect = pygame.Rect(screen.get_width()//2-__keyboardSize(size)[0]//2,size/2*1.7,keyboard_width,screen.get_height()*0.3)
    inRect = pygame.Rect(rect.x+margin,rect.y+margin,rect.width-(margin*2),rect.height-(margin*2))
    gfxdraw.box(screen,rect,Color.green)
    gfxdraw.box(screen,inRect,Color.black)
    x = rect.x + margin * 8
    y = rect.y + margin * 8
    __text(x, y, size, __typed_text, Color.green if __chosencode.startswith(__typed_text) else Color.red)
    __text(x, y, size, __chosencode, Color.green if __chosencode.startswith(__typed_text) else Color.red, opacity=50)


def main():
    global __typed_text, __chosencode
    clock = pygame.time.Clock()

    size = round(screen.get_rect().width * 0.045)
    kx = screen.get_rect().centerx - __keyboardSize(size)[0] / 2
    ky = screen.get_rect().centery - __keyboardSize(size)[1] / 2

    channelid = 0
    mixer.init()
    for i in range(8): mixer.Channel(i).set_volume(0.2)
    mixer.set_num_channels(9)

    run = True
    while run:
        clock.tick(60)
        screen.fill(Color.black)

        __keyboard(kx, ky * 1.7, size)
        __textScreen(size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                ln = len(__typed_text)
                match event.key:
                    case pygame.K_ESCAPE: run = False
                    case pygame.K_BACKSPACE: __typed_text = __typed_text[:-1]
                    case pygame.K_RETURN:
                        if __typed_text == __chosencode:
                            mixer.Channel(8).play(Sound.rowc)
                            __typed_text = ""
                            __chosencode = random.choice(__codes)
                        else:
                            mixer.Channel(8).set_volume(0.2)
                            mixer.Channel(8).play(Sound.lost)
                            clock.tick(1)
                            run = False
                    case _: __typed_text += event.unicode
                if len(__typed_text) != ln:
                    mixer.Channel(channelid).play(Sound.key)
                    channelid += channelid*-1 if channelid >= 7 else 1


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
