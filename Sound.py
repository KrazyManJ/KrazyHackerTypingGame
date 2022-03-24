from pygame import mixer
from typing import Final
import os

mixer.init()
for i in range(8):
    mixer.Channel(i).set_volume(0.2)
mixer.set_num_channels(9)


def _sound(soundname) -> mixer.Sound:
    return mixer.Sound(os.path.join("src", "sounds", soundname))


key: Final = _sound("typing.mp3")
rowc: Final = _sound("row_complete.wav")
lost: Final = _sound("lost.wav")

CHANNEL_ID = 0


def play(sound: mixer.Sound, volume: float = 0.2):
    global CHANNEL_ID
    mixer.Channel(CHANNEL_ID).play(sound)
    mixer.Channel(CHANNEL_ID).set_volume(volume)
    CHANNEL_ID += CHANNEL_ID * -1 if CHANNEL_ID >= 7 else 1
