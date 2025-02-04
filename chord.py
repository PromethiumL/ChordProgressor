import copy
import random

from chord_transforms import (
    ChordTransformationStrategy,
    Drop1,
    Drop2,
    Drop3,
    Drop23,
    Drop24,
)
from constants import (
    _CHORD_INTERVALS,
    _INTERVAL_SIZE,
)
from note import Note
from utils import is_valid_chord_name, is_valid_note_name

import typing

if typing.TYPE_CHECKING:
    from voice_leading import VoiceLeadingAlgorithm


class Chord:
    """Note-based chord representation."""

    def __init__(self, pitch_class_name: str = 'C'):
        self.available_transforms: list[ChordTransformationStrategy] = [
            Drop1(),
            Drop2(),
            Drop3(),
            Drop23(),
            Drop24(),
        ]

        # If input is just a valid note name (e.g. 'C', 'F#'), create a major triad
        if is_valid_note_name(pitch_class_name):
            self.root = Note(pitch_class_name)
            self.type = 'maj'
            self.name = self.root.name
            self.intervals = _CHORD_INTERVALS[self.type]
            self.build_chord()
            return

        # Check for empty input
        if len(pitch_class_name) < 1:
            raise Exception('incorrect chord name: {}'.format(pitch_class_name))

        # Try to extract root note from first two chars (e.g. 'C#' from 'C#m7')
        note_name = pitch_class_name[:2]
        if is_valid_note_name(note_name):
            self.root = Note(note_name)
            self.type = pitch_class_name[2:]  # Rest is chord type
        # Try single char root (e.g. 'C' from 'Cm7')
        elif is_valid_note_name(note_name[0]):
            self.root = Note(note_name[0])
            self.type = pitch_class_name[1:]  # Rest is chord type
        else:
            raise Exception('unrecognized root')

        # Validate the extracted chord type
        self.type = self.type.replace('^', 'Maj')
        self.type = self.type.replace('maj', 'Maj')
        if self.type[0] == '-':
            self.type = 'm' + self.type[1:]

        if not is_valid_chord_name(self.type):
            note_name = 'unrecognized chord type: root: {}, type: {}'.format(
                self.root.name, self.type
            )
            raise Exception(note_name)

        self.intervals = _CHORD_INTERVALS[self.type]
        self.name = pitch_class_name
        self.build_chord()
        self.expand()

    def build_chord(self) -> None:
        lower = copy.deepcopy(self.root)
        lower.move_by_one_octave_downward()

        self.notes: list[Note] = []
        self.notes.append(lower)
        self.notes.append(self.root)  # These are the two root notes.

        for n in self.intervals:
            new_note = copy.deepcopy(self.root)
            new_note.increment(_INTERVAL_SIZE[n])  # construct chord notes
            self.notes.sort()
            self.notes.append(new_note)

        self.intervals = self.notes[1:]  # Now base is an array of notes.

    def remove_duplicate_notes(self) -> None:
        unique_notes = list({note.index: note for note in self.notes}.values())
        unique_notes.sort()
        self.notes = unique_notes

    def __repr__(self) -> str:
        return 'name: {}, root: {}, type: {}\n\tNote list: {}'.format(
            self.name, self.root.name, self.type, list(map(lambda x: x.name, self.notes))
        )

    def show_info(self) -> None:
        print(self.__repr__())

    def invert_chord_up(self) -> None:
        bottom_note = self.intervals[0]
        self.intervals = self.intervals[1:]
        bottom_note.move_by_one_octave_upward()
        self.intervals.append(bottom_note)
        self.intervals.sort()
        self.remove_duplicate_notes()

    def apply_chord_transform(self, transform: ChordTransformationStrategy) -> None:
        transform.apply(self)

    def expand(self, gap: int = 5) -> None:  # gap 5 means M3
        """Expand the chord voicing to be more open.

        Args:
            gap: Minimum interval size between adjacent notes (default 5 for major third)
        """
        self.notes.sort()

        # Threshold to avoid extremely high notes
        max_voicing_note_index = 65

        i = 2
        while i < (len(self.notes) - 1):  # allow m2 in the ending
            # Check if interval between current and previous note is less than minimum gap
            # TODO: randomness
            gap = random.choices([5, 3, 6], weights=[0.6, 0.2, 0.2])[0]

            if (self.notes[i].index - self.notes[i - 1].index) >= gap:
                # Interval is wide enough, increment by 2 to avoid too wide arrangement
                i += 2
                continue

            try:
                self.notes[i].move_by_one_octave_upward()
                if self.notes[i].index > max_voicing_note_index:
                    raise Exception(f'A note ({self.notes[i].index}) is out of range.')
            except Exception:
                del self.notes[i]

            self.notes.sort()

    def connect_to(self, target: 'Chord', method: 'VoiceLeadingAlgorithm | None' = None) -> None:
        """Connect this chord to a target chord using a specified voice-leading algorithm."""
        if method is None:
            from voice_leading import DefaultVoiceLeading

            method = DefaultVoiceLeading()

        self.notes = method.solve(self, target)
