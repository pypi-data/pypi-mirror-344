from enum import Enum


class ParentItemType(str, Enum):
    ARTICLEMETADATA = "ArticleMetadata"
    REDDITCOMMENTMETADATA = "RedditCommentMetadata"
    REDDITPOSTMETADATA = "RedditPostMetadata"
    YOUTUBECOMMENTMETADATA = "YoutubeCommentMetadata"
    YOUTUBESEARCHMETADATA = "YoutubeSearchMetadata"
    YOUTUBEVIDEOMETADATA = "YoutubeVideoMetadata"

    def __str__(self) -> str:
        return str(self.value)
