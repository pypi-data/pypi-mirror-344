from enum import Enum


class SearchBarType(str, Enum):
    SUBREDDIT_INFO = "subreddit_info"
    YOUTUBE_CHANNEL_INFO = "youtube_channel_info"

    def __str__(self) -> str:
        return str(self.value)
