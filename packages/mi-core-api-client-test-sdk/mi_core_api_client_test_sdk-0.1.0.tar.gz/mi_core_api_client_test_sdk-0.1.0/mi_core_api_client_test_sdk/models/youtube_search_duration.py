from enum import Enum


class YoutubeSearchDuration(str, Enum):
    LONG = "long"
    MEDIUM = "medium"
    SHORT = "short"

    def __str__(self) -> str:
        return str(self.value)
