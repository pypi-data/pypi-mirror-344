from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.youtube_videos_request_youtube_channels import YoutubeVideosRequestYoutubeChannels


T = TypeVar("T", bound="YoutubeVideosRequest")


@_attrs_define
class YoutubeVideosRequest:
    """
    Attributes:
        youtube_channels (YoutubeVideosRequestYoutubeChannels):
    """

    youtube_channels: "YoutubeVideosRequestYoutubeChannels"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        youtube_channels = self.youtube_channels.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "youtube_channels": youtube_channels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.youtube_videos_request_youtube_channels import YoutubeVideosRequestYoutubeChannels

        d = dict(src_dict)
        youtube_channels = YoutubeVideosRequestYoutubeChannels.from_dict(d.pop("youtube_channels"))

        youtube_videos_request = cls(
            youtube_channels=youtube_channels,
        )

        youtube_videos_request.additional_properties = d
        return youtube_videos_request

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
