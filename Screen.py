from itertools import cycle

from typing import Final
import pygame
from pygame import gfxdraw

import Color
import Keyboard
import GraphUtils

CARET_COLORS: Final = [Color.green, Color.black]
CARET_CYCLE: Final = cycle(CARET_COLORS)

CARET_CURRENT_COLOR = next(CARET_CYCLE)


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

    cursor = pygame.Rect(x, y, Keyboard.KEY_LABEL_SIZE // 2, Keyboard.KEY_LABEL_SIZE)
    cursor.midleft = text_rect.midright
    gfxdraw.box(surface, cursor, CARET_CURRENT_COLOR)


def update_caret():
    global CARET_CURRENT_COLOR
    CARET_CURRENT_COLOR = CARET_COLORS[0]
    pass


def switch_caret():
    global CARET_CURRENT_COLOR
    CARET_CURRENT_COLOR = next(CARET_CYCLE)
