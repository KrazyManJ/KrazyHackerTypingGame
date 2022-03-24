import os
import random

import pygame
from pygame import time, display

import Color
import Keyboard
import Sound
import Screen

pygame.init()
display.set_icon(pygame.image.load(os.path.join("src", "krazyhackertypinggame.png")))
display.set_caption("KrazyHackerTypingGame", os.path.join("src", "krazyhackertypinggame.png"))
win = display.set_mode((0, 0), pygame.FULLSCREEN) if False else display.set_mode((1280, 720))

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
