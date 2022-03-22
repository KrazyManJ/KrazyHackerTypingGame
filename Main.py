import os
import random
from itertools import cycle
from typing import Final

import pygame
from pygame import gfxdraw, mixer, Rect, freetype, time, display

pygame.init()
display.set_icon(pygame.image.load(os.path.join("src", "krazyhackertypinggame.png")))
display.set_caption("KrazyHackerTypingGame", os.path.join("src", "krazyhackertypinggame.png"))
win = display.set_mode((0, 0), pygame.FULLSCREEN) if False else display.set_mode((1280, 720))


class Color:
    white: Final = (255, 255, 255)
    light_gray: Final = (128, 128, 128)
    black: Final = (0, 0, 0)
    green: Final = (0, 255, 0)
    red: Final = (255, 0, 0)
    gray: Final = (0, 70, 0)
    shadow: Final = (0, 255, 0, 60)


class Sound:
    @staticmethod
    def _sound(soundname) -> mixer.Sound:
        return mixer.Sound(os.path.join("src", "sounds", soundname))

    key: Final = _sound("typing.mp3")
    rowc: Final = _sound("row_complete.wav")
    lost: Final = _sound("lost.wav")


class Keyboard:
    @staticmethod
    def __a(name, size, label, key=None, font="fira code") -> dict:
        return {"name": name, "size": size, "label": label, "font": font, "key": key}

    KEY_SIZE: Final = win.get_rect().width * 0.0455
    KEY_THICK: Final = KEY_SIZE // 20
    KEY_GAP: Final = KEY_SIZE // 10
    KEY_LABEL_SIZE: Final = KEY_SIZE // 2.5
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

    @staticmethod
    def __getpressedkeys():
        keys, tkey = pygame.key.get_pressed(), []
        for key in range(len(keys)):
            if keys[key]:
                tkey.append(pygame.key.name(key))
        return tkey

    @staticmethod
    def __key(key, x, y, color, sx=KEY_SIZE, label=None, pr=None, font="fira code"):
        rect = GraphUtils.draw_rect(x, y, sx, Keyboard.KEY_SIZE, color, Keyboard.KEY_THICK,
                                    invert=Keyboard.__getpressedkeys().__contains__(key) or pr)
        GraphUtils.draw_text_f(font, label if label is not None else key.upper(), Keyboard.KEY_LABEL_SIZE, rect,
                               Color.black if Keyboard.__getpressedkeys().__contains__(key) or pr else color)

    @staticmethod
    def __enter(x, y, color):
        width = 1.5

        colors = [color, Color.black] if Keyboard.__getpressedkeys().__contains__("return") else [Color.black, color]
        lowerwidth = Keyboard.size()[0] - Keyboard.rowsize(2) - Keyboard.KEY_GAP * 2

        rect = Rect(x, y, lowerwidth, Keyboard.KEY_SIZE * 2 + Keyboard.KEY_GAP)
        recti = Rect(x + Keyboard.KEY_THICK, y + Keyboard.KEY_THICK, rect.width - Keyboard.KEY_THICK * 2,
                     rect.height - Keyboard.KEY_THICK * 2)
        rect2 = GraphUtils.draw_rect(x, y, width * Keyboard.KEY_SIZE + (width - 1) * Keyboard.KEY_GAP,
                                     Keyboard.KEY_SIZE, colors[1], Keyboard.KEY_THICK)
        cord = list(rect2.topright)
        cord[0] = cord[0] + Keyboard.KEY_THICK
        cord[1] = cord[1] - Keyboard.KEY_THICK
        rect.topright = tuple(cord)
        recti.center = rect.center
        gfxdraw.box(win, rect, colors[1])
        gfxdraw.box(win, recti, colors[0])
        gfxdraw.box(win, rect2, colors[0])
        GraphUtils.draw_text_f("cambria", "⏎", Keyboard.KEY_LABEL_SIZE, rect, colors[1])

    @staticmethod
    def __pressed(modd) -> bool:
        if type(modd) is None:
            return False
        elif type(modd) == int:
            return pygame.key.get_mods() & modd
        else:
            return Keyboard.__getpressedkeys().__contains__(modd)

    @staticmethod
    def draw(x: int, y: int, color: tuple[int, int, int]):
        tx = x
        for rows in Keyboard.LAYOUT:
            for key in rows:
                if type(key) == list:
                    for k in key:
                        Keyboard.__key(k, tx, y, color)
                        tx += Keyboard.KEY_SIZE + Keyboard.KEY_GAP
                elif type(key) == dict:
                    s = key["size"] * Keyboard.KEY_SIZE + (key["size"] - 1) * Keyboard.KEY_GAP
                    Keyboard.__key(key["name"], tx, y, color, s, label=key["label"], font=key["font"],
                                   pr=Keyboard.__pressed(key["key"]))
                    tx += s + Keyboard.KEY_GAP
                elif key == "enter":
                    Keyboard.__enter(tx, y, color)
            tx = x
            y += Keyboard.KEY_GAP + Keyboard.KEY_SIZE

    @staticmethod
    def size() -> tuple[float, float]:
        s = 0
        for i in range(len(Keyboard.LAYOUT)):
            s = Keyboard.rowsize(i) if Keyboard.rowsize(i) > s else s
        x = s + Keyboard.KEY_GAP
        y = len(Keyboard.LAYOUT) * Keyboard.KEY_SIZE + ((len(Keyboard.LAYOUT) - 1) * Keyboard.KEY_GAP)
        return x, y

    @staticmethod
    def rowsize(index) -> float:
        t = 0
        for key in Keyboard.LAYOUT[index]:
            if type(key) is list:
                t += len(key) * Keyboard.KEY_SIZE + (len(key) - 1) * Keyboard.KEY_GAP
            elif type(key) is dict:
                t += key["size"] * Keyboard.KEY_SIZE + (key["size"] - 1) * Keyboard.KEY_GAP
        return t


class GraphUtils:
    @staticmethod
    def draw_rect(x, y, width, height, color: tuple[int, int, int], thickness, invert: bool = False) -> Rect:
        if invert:
            rect = Rect(x + thickness, y + thickness, width - thickness * 2, height - thickness * 2)
            gfxdraw.box(win, rect, color)
            return rect
        else:
            rect = Rect(x, y, width, height)
            for i in range(round(thickness)):
                gfxdraw.rectangle(win, rect, color)
                rect.x += 1
                rect.y += 1
                rect.width -= 2
                rect.height -= 2
            return rect

    @staticmethod
    def draw_text_f(font, text, size, rect, color):
        ft = freetype.SysFont(font, size)
        r = ft.get_rect(text, size=size)
        r.center = rect.center
        ft.render_to(win, r, text, color)


BLINK_EVENT = pygame.USEREVENT + 0
BLINK_SURFACES = cycle([Color.green, Color.black])
BLINK_SURFACE = next(BLINK_SURFACES)

__typed_text = ""


def __codescreen(x, y):
    rect = GraphUtils.draw_rect(x, y * 0.3, Keyboard.size()[0], Keyboard.size()[1] / 2, Color.green, Keyboard.KEY_THICK)
    console_rect = GraphUtils.draw_rect(rect.bottomleft[0] - Keyboard.KEY_THICK,
                                        rect.bottomleft[1] - Keyboard.KEY_THICK, Keyboard.size()[0], Keyboard.KEY_SIZE,
                                        Color.green, Keyboard.KEY_THICK)

    font = pygame.font.SysFont("fira code", round(Keyboard.KEY_LABEL_SIZE))
    text = font.render(__typed_text, True, Color.white)
    text_rect = text.get_rect()
    text_rect.midleft = console_rect.midleft
    text_rect.x = text_rect.x + Keyboard.KEY_GAP
    win.blit(text, text_rect)

    cursor = Rect(x, y, Keyboard.KEY_LABEL_SIZE // 2, Keyboard.KEY_LABEL_SIZE)
    cursor.midleft = text_rect.midright
    gfxdraw.box(win, cursor, BLINK_SURFACE)


def main():
    global __typed_text, BLINK_SURFACE
    time.set_timer(BLINK_EVENT, 500)
    clock = pygame.time.Clock()
    kx, ky = win.get_rect().centerx - Keyboard.size()[0] // 2, win.get_rect().centery - Keyboard.size()[1] // 2
    channelid = 0
    mixer.init()
    for i in range(8):
        mixer.Channel(i).set_volume(0.2)
    mixer.set_num_channels(9)
    run = True
    while run:
        clock.tick(60)
        win.fill(Color.black)
        Keyboard.draw(kx, ky * 1.7, Color.green)
        __codescreen(kx, ky)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == BLINK_EVENT:
                BLINK_SURFACE = next(BLINK_SURFACES)
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
                        if len(event.unicode) > 0 and ord(event.unicode) > 31:
                            __typed_text += event.unicode
                if len(__typed_text) != ln:
                    mixer.Channel(channelid).play(Sound.key)
                    mixer.Channel(channelid).set_volume(random.uniform(0.1, 0.2))
                    channelid += channelid * -1 if channelid >= 7 else 1
                    BLINK_SURFACE = Color.green
        display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
