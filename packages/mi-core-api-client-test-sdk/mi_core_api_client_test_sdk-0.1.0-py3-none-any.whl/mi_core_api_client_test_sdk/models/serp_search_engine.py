from enum import Enum


class SerpSearchEngine(str, Enum):
    GOOGLE = "google"
    YOUTUBE = "youtube"

    def __str__(self) -> str:
        return str(self.value)
