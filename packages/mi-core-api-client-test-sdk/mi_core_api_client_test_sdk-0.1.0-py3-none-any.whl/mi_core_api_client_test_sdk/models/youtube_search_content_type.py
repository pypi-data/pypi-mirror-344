from enum import Enum


class YoutubeSearchContentType(str, Enum):
    CHANNEL = "channel"
    MOVIE = "movie"
    PLAYLIST = "playlist"
    VIDEO = "video"

    def __str__(self) -> str:
        return str(self.value)
