import pygame as pg
import time
import music


def init():
    pg.mixer.pre_init(44100, -16, 2, 2048)  # avoid the lag
    pg.mixer.init()
    pg.init()
    pg.mixer.set_num_channels(50)
    print('Module \'playsound\' loaded.')


def play(notes, interval=0, duration=5):
    """Play the notes at once. """

    if notes is None:
        time.sleep(duration)
        return

    queue = []
    if isinstance(notes, music.Chord):
        notes = notes.notes

    if type(notes) == list:
        if len(notes) == 0:
            time.sleep(duration)
            return
        if isinstance(notes[0], music.Note):
            arr = []
            for n in notes:
                arr.append(n.index)
            notes = arr
        elif isinstance(notes[0], int):
            arr = notes
        else:
            print(notes[0])
            raise Exception("Unknown note type")
    else:
        if isinstance(notes, music.Note):
            arr = [notes.index]
        else:
            arr = [notes]

    for i in arr:
        #print('i = {}'.format(i))
        filename = './sounds/{}.wav'.format(i + 1)
        # print('playing \'' + filename + '\'...')
        queue.append(pg.mixer.Sound(filename))
    for n in queue:
        n.play()
        time.sleep(interval)
    time.sleep(duration)
    del queue


def main():
    c1 = music.Chord('Dm7')
    play(c1, interval=0.1)


if __name__ == '__main__':
    init()
    main()

if __name__ == 'playsound':
    init()
