from enum import Enum


class ServiceType(str, Enum):
    ARTICLE = "Article"
    REDDIT = "Reddit"
    YOUTUBE = "Youtube"

    def __str__(self) -> str:
        return str(self.value)
