import typing

if typing.TYPE_CHECKING:
    from chord import Chord


class ChordTransformationStrategy(typing.Protocol):
    def apply(self, chord: 'Chord') -> None:
        raise NotImplementedError("This method should be overridden in subclasses.")


class Drop1(ChordTransformationStrategy):
    def apply(self, chord: 'Chord') -> None:
        chord.notes[-1].move_by_one_octave_downward()
        chord.remove_duplicate_notes()


class Drop2(ChordTransformationStrategy):
    def apply(self, chord: 'Chord') -> None:
        chord.notes[-2].move_by_one_octave_downward()
        chord.remove_duplicate_notes()


class Drop3(ChordTransformationStrategy):
    def apply(self, chord: 'Chord') -> None:
        if len(chord.notes) < 5:
            chord.notes[-2].move_by_one_octave_downward()
        else:
            chord.notes[-3].move_by_one_octave_downward()
        chord.remove_duplicate_notes()


class Drop23(ChordTransformationStrategy):
    def apply(self, chord: 'Chord') -> None:
        if len(chord.notes) < 5:
            chord.notes[-2].move_by_one_octave_downward()
        else:
            chord.notes[-2].move_by_one_octave_downward()
            chord.notes[-3].move_by_one_octave_downward()
        chord.remove_duplicate_notes()


class Drop24(ChordTransformationStrategy):
    def apply(self, chord: 'Chord') -> None:
        if len(chord.notes) < 6:
            chord.notes[-2].move_by_one_octave_downward()
            chord.notes[-3].move_by_one_octave_downward()
        else:
            chord.notes[-2].move_by_one_octave_downward()
            chord.notes[-4].move_by_one_octave_downward()
        chord.remove_duplicate_notes()
