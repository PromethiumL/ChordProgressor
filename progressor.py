from chord import Chord
from sound_engine import SoundEngine
from pygame_output import PyGameOutput
import random

# Initialize the sound engine with PyGameOutput
engine = SoundEngine(PyGameOutput())


def play_random_connected_chords():
    chord_names = 'Ebmaj7,Fm7,Fo7,G7,Abmaj7,Ab7,Gm,Bb7,Cm7,Do7,Dbmaj7'.split(',')

    previous_chord = Chord(chord_names[0])
    chord_list = []
    for name in chord_names:
        chord_list.append(Chord(name))

    for _ in range(200):
        current_chord = random.choice(chord_list)
        current_chord.connect_to(previous_chord)
        current_chord.show_info()
        for _ in range(1):
            engine.play(current_chord, interval=0.04, duration=1)
        previous_chord = current_chord


def read_chord_from_stdin_interactively():
    current_chord = Chord('Cmaj7')
    current_chord.expand()
    while True:
        try:
            chord_input = input('> ')
            new_chord = Chord(chord_input)
            new_chord.connect_to(current_chord)
            current_chord = new_chord
            engine.play(new_chord, interval=0.1, duration=0.2)
        except Exception as e:
            print(e)


def progress_with_connection():
    chord_sequence = (
        # Giant steps
        "Bmaj7,D7,Gmaj7,Bb7,Ebmaj7,Ebmaj7,Am7,D7,"
        "Gmaj7,Bb7,Ebmaj7,Gb7,Bmaj7,Bmaj7,Fm7,Bb7,"
        "Ebmaj7,Ebmaj7,Am7,D7,"
        "Gmaj7,Gmaj7,Dbm7,Gb7,"
        "Bmaj7,Bmaj7,Fm7,Bb7,"
        "Ebmaj7,Ebmaj7,D7,D7".split(',')
    )
    chord_sequence *= 2
    previous_chord = Chord(chord_sequence[0])
    for name in chord_sequence:
        current_chord = Chord(name)
        current_chord.connect_to(previous_chord)
        current_chord.show_info()
        previous_chord = current_chord
        engine.play(current_chord, interval=0.05, duration=0.5)


if __name__ == "__main__":
    progress_with_connection()
    # play_random_connected_chords()
    # read_chord_from_stdin_interactively()
