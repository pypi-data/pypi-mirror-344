from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SubredditAverageValues")


@_attrs_define
class SubredditAverageValues:
    """
    Attributes:
        average_upvotes (int):
        upvotes_range (str):
        average_comments (int):
        comments_range (str):
        average_word_count (int):
        word_count_range (str):
        total_posts (int):
    """

    average_upvotes: int
    upvotes_range: str
    average_comments: int
    comments_range: str
    average_word_count: int
    word_count_range: str
    total_posts: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        average_upvotes = self.average_upvotes

        upvotes_range = self.upvotes_range

        average_comments = self.average_comments

        comments_range = self.comments_range

        average_word_count = self.average_word_count

        word_count_range = self.word_count_range

        total_posts = self.total_posts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "averageUpvotes": average_upvotes,
                "upvotesRange": upvotes_range,
                "averageComments": average_comments,
                "commentsRange": comments_range,
                "averageWordCount": average_word_count,
                "wordCountRange": word_count_range,
                "totalPosts": total_posts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        average_upvotes = d.pop("averageUpvotes")

        upvotes_range = d.pop("upvotesRange")

        average_comments = d.pop("averageComments")

        comments_range = d.pop("commentsRange")

        average_word_count = d.pop("averageWordCount")

        word_count_range = d.pop("wordCountRange")

        total_posts = d.pop("totalPosts")

        subreddit_average_values = cls(
            average_upvotes=average_upvotes,
            upvotes_range=upvotes_range,
            average_comments=average_comments,
            comments_range=comments_range,
            average_word_count=average_word_count,
            word_count_range=word_count_range,
            total_posts=total_posts,
        )

        subreddit_average_values.additional_properties = d
        return subreddit_average_values

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
