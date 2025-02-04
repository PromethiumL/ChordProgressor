import time

from chord import Chord
from note import Note
from media_output import MediaOutput


class SoundEngine:
    def __init__(self, output: MediaOutput):
        self.output = output
        self.output.init()

    def play(self, notes: Chord | Note | list[Note | int] | int, interval=0, duration=5):
        """Play the notes at once."""

        # Handle empty/None cases
        if notes is None or (isinstance(notes, list) and len(notes) == 0):
            time.sleep(duration)
            return

        # Convert Chord object to list of notes
        if isinstance(notes, Chord):
            notes = notes.notes

        # Convert single Note/int to list
        if not isinstance(notes, list):
            notes = [notes]

        # Get note indices based on input type
        note_indices = []
        first_note = notes[0]

        if isinstance(first_note, Note):
            note_indices = [n.index for n in notes]
        elif isinstance(first_note, int):
            note_indices = notes
        else:
            print(first_note)
            raise Exception("Unknown note type")

        # Use the media output to play notes
        self.output.play_notes(note_indices, interval, duration)


def main():
    from pygame_output import PyGameOutput

    engine = SoundEngine(PyGameOutput())
    chord = Chord('Dm7')
    engine.play(chord, interval=0.1)


if __name__ == '__main__':
    main()
