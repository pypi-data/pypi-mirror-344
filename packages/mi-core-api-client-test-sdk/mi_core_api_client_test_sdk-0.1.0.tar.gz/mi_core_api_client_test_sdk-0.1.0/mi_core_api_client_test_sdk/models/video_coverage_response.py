from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.yt_channel_coverage import YTChannelCoverage


T = TypeVar("T", bound="VideoCoverageResponse")


@_attrs_define
class VideoCoverageResponse:
    """
    Attributes:
        generation_topic (str):
        youtube_channels (list['YTChannelCoverage']):
    """

    generation_topic: str
    youtube_channels: list["YTChannelCoverage"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        generation_topic = self.generation_topic

        youtube_channels = []
        for youtube_channels_item_data in self.youtube_channels:
            youtube_channels_item = youtube_channels_item_data.to_dict()
            youtube_channels.append(youtube_channels_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "generationTopic": generation_topic,
                "youtubeChannels": youtube_channels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.yt_channel_coverage import YTChannelCoverage

        d = dict(src_dict)
        generation_topic = d.pop("generationTopic")

        youtube_channels = []
        _youtube_channels = d.pop("youtubeChannels")
        for youtube_channels_item_data in _youtube_channels:
            youtube_channels_item = YTChannelCoverage.from_dict(youtube_channels_item_data)

            youtube_channels.append(youtube_channels_item)

        video_coverage_response = cls(
            generation_topic=generation_topic,
            youtube_channels=youtube_channels,
        )

        video_coverage_response.additional_properties = d
        return video_coverage_response

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
