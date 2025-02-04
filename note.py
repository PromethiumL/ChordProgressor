from constants import (
    _C_NOTE_OFFSET,
    _INT_TO_PITCH_CLASSES,
    _INTERVAL_SIZE,
    _MAX_NOTE_INDEX,
    _PITCH_CLASS_NAME_TO_INT,
)


def select_note_name(name: str | tuple, flag: int) -> str:
    """Selects the appropriate note name based on the accidental flag."""
    if flag > 0:
        return name[0]

    return name[1]


class Note:
    """Music note class."""

    accidental_flag: int = 0

    def __init__(self, name: str | None = None, octave: int = 2, index: int | None = None):
        "Note constructor"
        if not (name is None) or (index is None):
            self.name = name
            self.octave = octave
            self.index = _C_NOTE_OFFSET + self.octave * 12 + _PITCH_CLASS_NAME_TO_INT[name]
        else:
            self.index = index
            self.name = None
            self.octave = (index + (12 - _C_NOTE_OFFSET)) // 12 + 1
        self.clamp_index()
        self._update_name()

    def increment(self, step: int | str = 1) -> None:
        if not isinstance(step, int):
            if step not in _INTERVAL_SIZE:
                raise Exception("increment step error: {}".format(step))
            else:
                step = _INTERVAL_SIZE[step]
        self.accidental_flag = 1
        self.index += step
        self.octave = (self.index - _C_NOTE_OFFSET + 12) // 12
        self.clamp_index()
        self._update_name()

    def decrement(self, step: int | str = 1) -> None:
        if not isinstance(step, int):
            if step not in _INTERVAL_SIZE:
                raise Exception("decrement step error")
            else:
                step = _INTERVAL_SIZE[step]

        self.accidental_flag = -1
        self.index -= step
        self.octave = (self.index - _C_NOTE_OFFSET + 12) // 12
        self.clamp_index()
        self._update_name()

    def _update_name(self) -> None:
        if self.name is not None:
            if 'b' in self.name:
                self.accidental_flag = -1
            if '#' in self.name:
                self.accidental_flag = 1

        self.name = _INT_TO_PITCH_CLASSES[(self.index - _C_NOTE_OFFSET) % 12]
        if len(self.name) > 1:
            self.name = select_note_name(self.name, self.accidental_flag)

    def clamp_index(self) -> None:
        if self.index < 0:
            self.index += 24
        if self.index > _MAX_NOTE_INDEX:
            self.index -= 24

    def __repr__(self) -> str:
        return "Note: name: {}, index: {},  octave: {}, accidental_flag: {}".format(
            self.name, self.index, self.octave, self.accidental_flag
        )

    def show_info(self) -> None:
        print(self.__repr__())

    def move_by_one_octave_upward(self) -> None:
        self.increment(12)
        self.clamp_index()

    def move_by_one_octave_downward(self) -> None:
        self.decrement(12)
        self.clamp_index()

    def __lt__(self, other: 'Note') -> bool:
        return self.index < other.index

    def __eq__(self, other: 'Note') -> bool:
        return self.index == other.index
