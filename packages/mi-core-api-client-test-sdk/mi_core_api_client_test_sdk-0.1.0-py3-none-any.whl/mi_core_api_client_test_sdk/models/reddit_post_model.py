from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RedditPostModel")


@_attrs_define
class RedditPostModel:
    """
    Attributes:
        title (str):
        link (str):
        published_date (str):
        body (str):
        author (str):
        subreddit (str):
        comments_count (Union[None, Unset, int]):
        upvotes (Union[None, Unset, int]):
    """

    title: str
    link: str
    published_date: str
    body: str
    author: str
    subreddit: str
    comments_count: Union[None, Unset, int] = UNSET
    upvotes: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        link = self.link

        published_date = self.published_date

        body = self.body

        author = self.author

        subreddit = self.subreddit

        comments_count: Union[None, Unset, int]
        if isinstance(self.comments_count, Unset):
            comments_count = UNSET
        else:
            comments_count = self.comments_count

        upvotes: Union[None, Unset, int]
        if isinstance(self.upvotes, Unset):
            upvotes = UNSET
        else:
            upvotes = self.upvotes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "link": link,
                "publishedDate": published_date,
                "body": body,
                "author": author,
                "subreddit": subreddit,
            }
        )
        if comments_count is not UNSET:
            field_dict["commentsCount"] = comments_count
        if upvotes is not UNSET:
            field_dict["upvotes"] = upvotes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        link = d.pop("link")

        published_date = d.pop("publishedDate")

        body = d.pop("body")

        author = d.pop("author")

        subreddit = d.pop("subreddit")

        def _parse_comments_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        comments_count = _parse_comments_count(d.pop("commentsCount", UNSET))

        def _parse_upvotes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        upvotes = _parse_upvotes(d.pop("upvotes", UNSET))

        reddit_post_model = cls(
            title=title,
            link=link,
            published_date=published_date,
            body=body,
            author=author,
            subreddit=subreddit,
            comments_count=comments_count,
            upvotes=upvotes,
        )

        reddit_post_model.additional_properties = d
        return reddit_post_model

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
