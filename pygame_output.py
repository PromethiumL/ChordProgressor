import pygame as pg
import time
from typing import List
from media_output import MediaOutput


class PyGameOutput(MediaOutput):
    def init(self) -> None:
        pg.mixer.pre_init(44100, -16, 2, 2048)  # avoid the lag
        pg.mixer.init()
        pg.init()
        pg.mixer.set_num_channels(50)
        print('PyGameOutput initialized.')

    def play_notes(self, note_indices: List[int], interval: float, duration: float) -> None:
        sound_queue = []
        for index in note_indices:
            filename = f'./sounds/{index + 1}.wav'
            sound_queue.append(pg.mixer.Sound(filename))

        for sound in sound_queue:
            sound.play()
            time.sleep(interval)

        time.sleep(duration)
        del sound_queue
