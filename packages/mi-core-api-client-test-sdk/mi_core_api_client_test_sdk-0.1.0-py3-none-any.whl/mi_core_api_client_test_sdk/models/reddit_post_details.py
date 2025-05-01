from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.author_schema import AuthorSchema
    from ..models.subreddit_schema import SubredditSchema


T = TypeVar("T", bound="RedditPostDetails")


@_attrs_define
class RedditPostDetails:
    """
    Attributes:
        post_id (str):
        title (str):
        body (str):
        body_urls (list[str]):
        author (AuthorSchema):
        lock_status (bool):
        comments_count (int):
        upvotes (int):
        subreddit (SubredditSchema):
    """

    post_id: str
    title: str
    body: str
    body_urls: list[str]
    author: "AuthorSchema"
    lock_status: bool
    comments_count: int
    upvotes: int
    subreddit: "SubredditSchema"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post_id = self.post_id

        title = self.title

        body = self.body

        body_urls = self.body_urls

        author = self.author.to_dict()

        lock_status = self.lock_status

        comments_count = self.comments_count

        upvotes = self.upvotes

        subreddit = self.subreddit.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "postId": post_id,
                "title": title,
                "body": body,
                "bodyUrls": body_urls,
                "author": author,
                "lockStatus": lock_status,
                "commentsCount": comments_count,
                "upvotes": upvotes,
                "subreddit": subreddit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.author_schema import AuthorSchema
        from ..models.subreddit_schema import SubredditSchema

        d = dict(src_dict)
        post_id = d.pop("postId")

        title = d.pop("title")

        body = d.pop("body")

        body_urls = cast(list[str], d.pop("bodyUrls"))

        author = AuthorSchema.from_dict(d.pop("author"))

        lock_status = d.pop("lockStatus")

        comments_count = d.pop("commentsCount")

        upvotes = d.pop("upvotes")

        subreddit = SubredditSchema.from_dict(d.pop("subreddit"))

        reddit_post_details = cls(
            post_id=post_id,
            title=title,
            body=body,
            body_urls=body_urls,
            author=author,
            lock_status=lock_status,
            comments_count=comments_count,
            upvotes=upvotes,
            subreddit=subreddit,
        )

        reddit_post_details.additional_properties = d
        return reddit_post_details

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
