from enum import Enum


class SourceTypes(str, Enum):
    ARTICLE = "article"
    ARTICLE_SEARCH = "article_search"
    REDDIT_POST = "reddit_post"
    REDDIT_SEARCH = "reddit_search"
    REDDIT_USER = "reddit_user"
    SUBREDDIT = "subreddit"
    YT_CHANNEL = "yt_channel"
    YT_SEARCH = "yt_search"
    YT_VIDEO = "yt_video"

    def __str__(self) -> str:
        return str(self.value)
