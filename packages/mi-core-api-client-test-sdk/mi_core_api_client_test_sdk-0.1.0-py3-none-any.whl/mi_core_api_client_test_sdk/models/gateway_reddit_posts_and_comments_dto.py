from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.reddit_comment_model import RedditCommentModel
    from ..models.reddit_post_model import RedditPostModel


T = TypeVar("T", bound="GatewayRedditPostsAndCommentsDTO")


@_attrs_define
class GatewayRedditPostsAndCommentsDTO:
    """
    Attributes:
        post (RedditPostModel):
        comments (list['RedditCommentModel']):
    """

    post: "RedditPostModel"
    comments: list["RedditCommentModel"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post = self.post.to_dict()

        comments = []
        for comments_item_data in self.comments:
            comments_item = comments_item_data.to_dict()
            comments.append(comments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "post": post,
                "comments": comments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reddit_comment_model import RedditCommentModel
        from ..models.reddit_post_model import RedditPostModel

        d = dict(src_dict)
        post = RedditPostModel.from_dict(d.pop("post"))

        comments = []
        _comments = d.pop("comments")
        for comments_item_data in _comments:
            comments_item = RedditCommentModel.from_dict(comments_item_data)

            comments.append(comments_item)

        gateway_reddit_posts_and_comments_dto = cls(
            post=post,
            comments=comments,
        )

        gateway_reddit_posts_and_comments_dto.additional_properties = d
        return gateway_reddit_posts_and_comments_dto

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
