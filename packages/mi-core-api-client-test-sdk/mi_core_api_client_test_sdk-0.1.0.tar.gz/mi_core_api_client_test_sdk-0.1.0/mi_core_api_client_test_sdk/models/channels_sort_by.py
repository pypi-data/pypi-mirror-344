from enum import Enum


class ChannelsSortBy(str, Enum):
    NONE = "none"
    SUBSCRIBERS = "subscribers"
    TOTAL_VIDEOS = "total_videos"
    TOTAL_VIEWS = "total_views"

    def __str__(self) -> str:
        return str(self.value)
