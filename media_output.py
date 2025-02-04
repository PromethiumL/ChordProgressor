from typing import Protocol


class MediaOutput(Protocol):
    def play_notes(self, note_indices: list[int], interval: float, duration: float) -> None:
        pass

    def init(self) -> None:
        pass
