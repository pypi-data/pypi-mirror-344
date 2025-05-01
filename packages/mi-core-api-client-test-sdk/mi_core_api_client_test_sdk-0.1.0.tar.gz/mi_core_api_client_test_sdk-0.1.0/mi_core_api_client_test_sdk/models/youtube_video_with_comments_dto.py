from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.youtube_comment_schema import YoutubeCommentSchema
    from ..models.youtube_video_schema import YoutubeVideoSchema


T = TypeVar("T", bound="YoutubeVideoWithCommentsDTO")


@_attrs_define
class YoutubeVideoWithCommentsDTO:
    """
    Attributes:
        video (YoutubeVideoSchema):
        comments (list['YoutubeCommentSchema']):
    """

    video: "YoutubeVideoSchema"
    comments: list["YoutubeCommentSchema"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        video = self.video.to_dict()

        comments = []
        for comments_item_data in self.comments:
            comments_item = comments_item_data.to_dict()
            comments.append(comments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "video": video,
                "comments": comments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.youtube_comment_schema import YoutubeCommentSchema
        from ..models.youtube_video_schema import YoutubeVideoSchema

        d = dict(src_dict)
        video = YoutubeVideoSchema.from_dict(d.pop("video"))

        comments = []
        _comments = d.pop("comments")
        for comments_item_data in _comments:
            comments_item = YoutubeCommentSchema.from_dict(comments_item_data)

            comments.append(comments_item)

        youtube_video_with_comments_dto = cls(
            video=video,
            comments=comments,
        )

        youtube_video_with_comments_dto.additional_properties = d
        return youtube_video_with_comments_dto

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
