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

    CHANNEL_ID = 0

    @staticmethod
    def register_mixer():
        mixer.init()
        for i in range(8):
            mixer.Channel(i).set_volume(0.2)
        mixer.set_num_channels(9)

    @staticmethod
    def play(sound: mixer.Sound, volume: float = 0.2):
        mixer.Channel(Sound.CHANNEL_ID).play(sound)
        mixer.Channel(Sound.CHANNEL_ID).set_volume(volume)
        Sound.CHANNEL_ID += Sound.CHANNEL_ID * -1 if Sound.CHANNEL_ID >= 7 else 1


class Keyboard:

    @staticmethod
    def init(size):
        Keyboard.KEY_SIZE = size
        Keyboard.KEY_THICK = Keyboard.KEY_SIZE // 20
        Keyboard.KEY_GAP = Keyboard.KEY_SIZE // 10
        Keyboard.KEY_LABEL_SIZE = Keyboard.KEY_SIZE // 2.5
        Keyboard.is_initialized()

    @staticmethod
    def is_initialized():
        if Keyboard.KEY_SIZE <= 0:
            raise ValueError("Keyboard is not initialized properly! Initialize it with positive number first!")

    @staticmethod
    def draw(surface, x: int, y: int, color: tuple[int, int, int]):
        Keyboard.is_initialized()
        tx = x
        for rows in Keyboard.LAYOUT:
            for key in rows:
                if type(key) == list:
                    for k in key:
                        Keyboard.__key(surface, k, tx, y, color, Keyboard.KEY_SIZE)
                        tx += Keyboard.KEY_SIZE + Keyboard.KEY_GAP
                elif type(key) == dict:
                    s = key["size"] * Keyboard.KEY_SIZE + (key["size"] - 1) * Keyboard.KEY_GAP
                    Keyboard.__key(surface, key["name"], tx, y, color, s, label=key["label"], font=key["font"],
                                   pr=Keyboard.__pressed(key["key"]))
                    tx += s + Keyboard.KEY_GAP
                elif key == "enter":
                    Keyboard.__enter(surface, tx, y, color)
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

    @staticmethod
    def __a(name, size, label, key=None, font="fira code") -> dict:
        return {"name": name, "size": size, "label": label, "font": font, "key": key}

    KEY_SIZE: int = 0
    KEY_THICK: int = KEY_SIZE // 20
    KEY_GAP: int = KEY_SIZE // 10
    KEY_LABEL_SIZE: int = KEY_SIZE // 2.5
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
    def __key(surface, key, x, y, color, sx, label=None, pr=None, font="fira code"):
        rect = GraphUtils.draw_rect(surface, x, y, sx, Keyboard.KEY_SIZE, color, Keyboard.KEY_THICK,
                                    invert=Keyboard.__getpressedkeys().__contains__(key) or pr)
        GraphUtils.draw_text_f(surface, font, label if label is not None else key.upper(),
                               Keyboard.KEY_LABEL_SIZE, rect,
                               Color.black if Keyboard.__getpressedkeys().__contains__(key) or pr else color)

    @staticmethod
    def __enter(surface, x, y, color):
        width = 1.5

        colors = [color, Color.black] if Keyboard.__getpressedkeys().__contains__("return") else [Color.black, color]
        lowerwidth = Keyboard.size()[0] - Keyboard.rowsize(2) - Keyboard.KEY_GAP * 2

        rect = Rect(x, y, lowerwidth, Keyboard.KEY_SIZE * 2 + Keyboard.KEY_GAP)
        recti = Rect(x + Keyboard.KEY_THICK, y + Keyboard.KEY_THICK, rect.width - Keyboard.KEY_THICK * 2,
                     rect.height - Keyboard.KEY_THICK * 2)
        rect2 = GraphUtils.draw_rect(surface, x, y, width * Keyboard.KEY_SIZE + (width - 1) * Keyboard.KEY_GAP,
                                     Keyboard.KEY_SIZE, colors[1], Keyboard.KEY_THICK)
        cord = list(rect2.topright)
        cord[0] = cord[0] + Keyboard.KEY_THICK
        cord[1] = cord[1] - Keyboard.KEY_THICK
        rect.topright = tuple(cord)
        recti.center = rect.center
        gfxdraw.box(surface, rect, colors[1])
        gfxdraw.box(surface, recti, colors[0])
        gfxdraw.box(surface, rect2, colors[0])
        GraphUtils.draw_text_f(surface, "cambria", "⏎", Keyboard.KEY_LABEL_SIZE, rect, colors[1])

    @staticmethod
    def __pressed(modd) -> bool:
        if type(modd) is None:
            return False
        elif type(modd) == int:
            return pygame.key.get_mods() & modd
        else:
            return Keyboard.__getpressedkeys().__contains__(modd)


class GraphUtils:
    @staticmethod
    def draw_rect(surface, x, y, width, height, color: tuple[int, int, int], thickness, invert: bool = False) -> Rect:
        if invert:
            rect = Rect(x + thickness, y + thickness, width - thickness * 2, height - thickness * 2)
            gfxdraw.box(surface, rect, color)
            return rect
        else:
            rect = Rect(x, y, width, height)
            for i in range(round(thickness)):
                gfxdraw.rectangle(surface, rect, color)
                rect.x += 1
                rect.y += 1
                rect.width -= 2
                rect.height -= 2
            return rect

    @staticmethod
    def draw_text_f(surface, font, text, size, rect, color):
        ft = freetype.SysFont(font, size)
        r = ft.get_rect(text, size=size)
        r.center = rect.center
        ft.render_to(surface, r, text, color)


class Screen:
    CARET_COLORS: Final = [Color.green, Color.black]
    CARET_CYCLE: Final = cycle(CARET_COLORS)

    CARET_CURRENT_COLOR = next(CARET_CYCLE)

    @staticmethod
    def draw(surface, x, y, typedtext):
        rect = GraphUtils.draw_rect(surface, x, y * 0.3, Keyboard.size()[0], Keyboard.size()[1] / 2, Color.green,
                                    Keyboard.KEY_THICK)
        console_rect = GraphUtils.draw_rect(surface, rect.bottomleft[0] - Keyboard.KEY_THICK,
                                            rect.bottomleft[1] - Keyboard.KEY_THICK, Keyboard.size()[0],
                                            Keyboard.KEY_SIZE,
                                            Color.green, Keyboard.KEY_THICK)

        font = pygame.font.SysFont("fira code", round(Keyboard.KEY_LABEL_SIZE))
        text = font.render(typedtext, True, Color.white)
        text_rect = text.get_rect()
        text_rect.midleft = console_rect.midleft
        text_rect.x = text_rect.x + Keyboard.KEY_GAP
        surface.blit(text, text_rect)

        cursor = Rect(x, y, Keyboard.KEY_LABEL_SIZE // 2, Keyboard.KEY_LABEL_SIZE)
        cursor.midleft = text_rect.midright
        gfxdraw.box(surface, cursor, Screen.CARET_CURRENT_COLOR)

    @staticmethod
    def update_caret():
        Screen.CARET_CURRENT_COLOR = Screen.CARET_COLORS[0]
        pass

    @staticmethod
    def switch_caret():
        Screen.CARET_CURRENT_COLOR = next(Screen.CARET_CYCLE)


if __name__ == "__main__":
    typed_text = ""
    BLINK_EVENT = pygame.USEREVENT + 0
    time.set_timer(BLINK_EVENT, 500)
    clock = pygame.time.Clock()

    Keyboard.init(win.get_rect().width * 0.0455)
    kx, ky = win.get_rect().centerx - Keyboard.size()[0] // 2, win.get_rect().centery - Keyboard.size()[1] // 2

    run = True
    while run:
        clock.tick(60)
        win.fill(Color.black)

        Keyboard.draw(win, kx, ky * 1.7, Color.green)
        Screen.draw(win, kx, ky, typed_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == BLINK_EVENT:
                Screen.switch_caret()
            elif event.type == pygame.KEYDOWN:
                ln = len(typed_text)
                match event.key:
                    case pygame.K_ESCAPE:
                        run = False
                    case pygame.K_BACKSPACE:
                        typed_text = typed_text[:-1]
                    case pygame.K_DELETE:
                        pass
                    case _:
                        if len(event.unicode) > 0 and ord(event.unicode) > 31:
                            typed_text += event.unicode
                if len(typed_text) != ln:
                    Sound.play(Sound.key, volume=random.uniform(0.1, 0.2))
                    Screen.update_caret()
        display.update()
    pygame.quit()
