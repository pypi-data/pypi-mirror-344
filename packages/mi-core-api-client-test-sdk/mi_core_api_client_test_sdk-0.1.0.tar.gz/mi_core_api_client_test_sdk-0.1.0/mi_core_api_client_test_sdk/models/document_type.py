from enum import Enum


class DocumentType(str, Enum):
    NEWS_ARTICLE = "news_article"
    REDDIT_COMMENT = "reddit_comment"
    REDDIT_POST = "reddit_post"
    SUBREDDIT_INFO = "subreddit_info"
    YOUTUBE_CHANNEL_INFO = "youtube_channel_info"
    YOUTUBE_COMMENT = "youtube_comment"
    YOUTUBE_VIDEO = "youtube_video"

    def __str__(self) -> str:
        return str(self.value)
