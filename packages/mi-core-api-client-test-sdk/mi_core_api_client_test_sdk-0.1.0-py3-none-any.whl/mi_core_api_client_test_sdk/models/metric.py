from enum import Enum


class Metric(str, Enum):
    BODY = "body"
    COMMENTS_COUNT = "comments_count"
    EST_REV = "est_rev"
    LIKES = "likes"
    MEMBERS = "members"
    ONLINE_MEMBERS = "online_members"
    POSTS_COMMENTS_COUNT = "posts_comments_count"
    POSTS_COUNT = "posts_count"
    POSTS_UPVOTES = "posts_upvotes"
    RANK = "rank"
    SUBSCRIBERS = "subscribers"
    TITLE = "title"
    TOTAL_VIDEOS = "total_videos"
    TOTAL_VIEWS = "total_views"
    UPVOTES = "upvotes"
    VIEWS = "views"

    def __str__(self) -> str:
        return str(self.value)
