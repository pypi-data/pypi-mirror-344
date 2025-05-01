from enum import Enum


class YoutubeSearchSortBy(str, Enum):
    DATE = "date"
    RATING = "rating"
    RELEVANCE = "relevance"
    VIEWS = "views"

    def __str__(self) -> str:
        return str(self.value)
