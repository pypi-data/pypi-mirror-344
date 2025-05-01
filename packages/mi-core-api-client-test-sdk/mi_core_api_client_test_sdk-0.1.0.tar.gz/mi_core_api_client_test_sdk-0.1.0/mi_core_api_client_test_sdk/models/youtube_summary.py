from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="YoutubeSummary")


@_attrs_define
class YoutubeSummary:
    """
    Attributes:
        views (int):
        videos_count (int):
        avg_likes (float):
        top_channel (str):
    """

    views: int
    videos_count: int
    avg_likes: float
    top_channel: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        views = self.views

        videos_count = self.videos_count

        avg_likes = self.avg_likes

        top_channel = self.top_channel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "views": views,
                "videosCount": videos_count,
                "avgLikes": avg_likes,
                "topChannel": top_channel,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        views = d.pop("views")

        videos_count = d.pop("videosCount")

        avg_likes = d.pop("avgLikes")

        top_channel = d.pop("topChannel")

        youtube_summary = cls(
            views=views,
            videos_count=videos_count,
            avg_likes=avg_likes,
            top_channel=top_channel,
        )

        youtube_summary.additional_properties = d
        return youtube_summary

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
