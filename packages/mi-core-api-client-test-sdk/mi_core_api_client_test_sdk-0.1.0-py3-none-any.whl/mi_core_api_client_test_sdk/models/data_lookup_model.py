from enum import Enum


class DataLookupModel(str, Enum):
    REDDITAUTHOR = "RedditAuthor"
    REDDITCOMMENT = "RedditComment"
    REDDITPOST = "RedditPost"
    SUBREDDITINFO = "SubredditInfo"
    YOUTUBECHANNELINFO = "YoutubeChannelInfo"
    YOUTUBECOMMENT = "YoutubeComment"
    YOUTUBEVIDEO = "YoutubeVideo"

    def __str__(self) -> str:
        return str(self.value)
