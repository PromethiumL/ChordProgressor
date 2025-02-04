import copy
from typing import Protocol
from chord import Chord

import functools


class VoiceLeadingAlgorithm(Protocol):
    def solve(self, src_chord: Chord, dest_chord: Chord) -> list[int]:
        pass


class DefaultVoiceLeading:
    def solve(self, src_chord: Chord, dest_chord: Chord) -> list[int]:
        chord_variations: list[tuple[int, Chord]] = []
        original_chord = copy.deepcopy(src_chord)

        for _ in range(len(src_chord.intervals) * 2):
            current_chord_inversion = copy.deepcopy(original_chord)

            for transform in src_chord.available_transforms:
                new_chord = copy.deepcopy(current_chord_inversion)
                new_chord.apply_chord_transform(transform)
                chord_variations.append((self.chord_dist_loss(new_chord, dest_chord), new_chord))

            original_chord.invert_chord_up()

        chord_variations = list(set(chord_variations))
        chord_variations.sort(key=lambda tp: tp[0])

        return chord_variations[0][1].notes

    def chord_dist(self, c1: Chord, c2: Chord) -> int:
        """Calculate the distance between two chords based on paired distances."""
        ts = [0, 0.2, 0.4, 0.6, 0.8, 1]
        dist = 0
        for t in ts:
            i1 = max(1, int(t * (len(c1.notes) - 1)))
            i2 = max(1, int(t * (len(c2.notes) - 1)))
            dist += (c1.notes[i1].index - c2.notes[i2].index) ** 2
        return dist

    def chord_dist_loss(self, chord: Chord, target: Chord) -> int:
        """The chord_dist_loss(x) to minimize"""
        weight_preferring_centered_voicing = 0.5
        return self.chord_dist(chord, target) + int(
            weight_preferring_centered_voicing
            * self.chord_dist(chord, get_standard_position_reference_chord())
        )


@functools.cache
def get_standard_position_reference_chord() -> Chord:
    chord = Chord('Cmaj7')
    chord.expand()
    for note in chord.notes[1:]:
        note.move_by_one_octave_upward()
    chord.show_info()
    return chord
