import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RedditPost")


@_attrs_define
class RedditPost:
    """
    Attributes:
        title (str):
        url (str):
        comments_count (int):
        upvotes (int):
        subreddit_name (str):
        published_date (datetime.datetime):
    """

    title: str
    url: str
    comments_count: int
    upvotes: int
    subreddit_name: str
    published_date: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        url = self.url

        comments_count = self.comments_count

        upvotes = self.upvotes

        subreddit_name = self.subreddit_name

        published_date = self.published_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "url": url,
                "commentsCount": comments_count,
                "upvotes": upvotes,
                "subredditName": subreddit_name,
                "publishedDate": published_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        url = d.pop("url")

        comments_count = d.pop("commentsCount")

        upvotes = d.pop("upvotes")

        subreddit_name = d.pop("subredditName")

        published_date = isoparse(d.pop("publishedDate"))

        reddit_post = cls(
            title=title,
            url=url,
            comments_count=comments_count,
            upvotes=upvotes,
            subreddit_name=subreddit_name,
            published_date=published_date,
        )

        reddit_post.additional_properties = d
        return reddit_post

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
