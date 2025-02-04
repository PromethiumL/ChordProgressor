from constants import _PITCH_CLASS_NAME_TO_INT, _CHORD_INTERVALS
import typing

if typing.TYPE_CHECKING:
    from note import Note


def is_valid_note_name(name: str) -> bool:
    return name in _PITCH_CLASS_NAME_TO_INT


def is_valid_chord_name(name: str) -> bool:
    return name in _CHORD_INTERVALS


def notes_have_same_name(i1: int, i2: int) -> bool:
    return i1 % 12 == i2 % 12


def compare_values(a: int, b: int) -> int:
    return (a > b) - (a < b)


def cmp_note_name(n1: 'Note', n2: 'Note') -> bool:  # TODO: unify naming. cmp and compare
    return _PITCH_CLASS_NAME_TO_INT[n1.name] == _PITCH_CLASS_NAME_TO_INT[n2.name]
