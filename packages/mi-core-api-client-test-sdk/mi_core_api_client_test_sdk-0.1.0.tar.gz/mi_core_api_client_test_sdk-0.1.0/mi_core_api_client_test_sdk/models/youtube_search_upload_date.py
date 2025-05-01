from enum import Enum


class YoutubeSearchUploadDate(str, Enum):
    LAST_HOUR = "last_hour"
    THIS_MONTH = "this_month"
    THIS_WEEK = "this_week"
    THIS_YEAR = "this_year"
    TODAY = "today"

    def __str__(self) -> str:
        return str(self.value)
