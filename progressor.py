#!/usr/bin/python

import sys
import playsound as ps
import time
import copy
import music
import random

# arr = ['Cmaj9','Am9', 'Dmaj11', 'D#o7', 'Em9', 'Do7', 'Ebmaj9', 'Dbmaj7']
# arr = ['Ab9', 'Db13', 'Gb9', 'B13', 'E9', 'A13', 'Dmaj9', None]
# arr = ['Dbmaj7', 'Dbm7', 'Cm7', 'Go7', 'Bbm7', 'Eb7', 'Abmaj7', None]
# arr = ['Bmaj7', 'D7', 'Gmaj7', 'Bb7', 'Ebmaj7',None, 'Am7', 'D7','Gmaj7', 'Bb7', 'Ebmaj7', 'F#7', 'Bmaj7',None, 'C#m7', 'F#7']


def randomlyplaywithconnection():
    arr = ['Ebmaj7', 'Fm7' , 'Fo7', 'G7', 'Abmaj7', 'Ab7', 'Gm', 'Bb7', 'Cm7', 'Do7', 'Dbmaj7']
    lastchord=music.Chord('Ebmaj7')
    l = []
    for ch in arr:
        l.append(music.Chord(ch))

    for i in range(20):
        ch = random.choice(l)
        ch.connect_to(lastchord)
        ch.show_info()
        for i in range(4):
            ps.play(ch ,interval=0, duration=1)
        lastchord = ch

def main():
    lastchord = music.Chord('Cmaj7')

    while 1:
        try:
            chord = raw_input('> ')
            chord = music.Chord(chord)
            chord.connect_to(lastchord)
            lastchord = chord
            ps.play(chord, interval=0.1, duration = 0.2)
        except Exception as e:
            print(e)



if __name__ == "__main__":
    #c1 = music.Chord('F13')
    #ps.play(c1, interval=0.15)
    main()
