from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.reddit_post_model import RedditPostModel
    from ..models.subreddit_info import SubredditInfo


T = TypeVar("T", bound="GatewaySubredditInfoWithLastPostDTO")


@_attrs_define
class GatewaySubredditInfoWithLastPostDTO:
    """
    Attributes:
        subreddit_info (SubredditInfo):
        last_posts (list['RedditPostModel']):
    """

    subreddit_info: "SubredditInfo"
    last_posts: list["RedditPostModel"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subreddit_info = self.subreddit_info.to_dict()

        last_posts = []
        for last_posts_item_data in self.last_posts:
            last_posts_item = last_posts_item_data.to_dict()
            last_posts.append(last_posts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subredditInfo": subreddit_info,
                "lastPosts": last_posts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reddit_post_model import RedditPostModel
        from ..models.subreddit_info import SubredditInfo

        d = dict(src_dict)
        subreddit_info = SubredditInfo.from_dict(d.pop("subredditInfo"))

        last_posts = []
        _last_posts = d.pop("lastPosts")
        for last_posts_item_data in _last_posts:
            last_posts_item = RedditPostModel.from_dict(last_posts_item_data)

            last_posts.append(last_posts_item)

        gateway_subreddit_info_with_last_post_dto = cls(
            subreddit_info=subreddit_info,
            last_posts=last_posts,
        )

        gateway_subreddit_info_with_last_post_dto.additional_properties = d
        return gateway_subreddit_info_with_last_post_dto

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
