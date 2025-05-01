from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.collect_youtube_channels_data_youtubechannels import CollectYoutubeChannelsDataYoutubechannels


T = TypeVar("T", bound="CollectYoutubeChannelsData")


@_attrs_define
class CollectYoutubeChannelsData:
    """
    Attributes:
        youtube_channels (CollectYoutubeChannelsDataYoutubechannels):
    """

    youtube_channels: "CollectYoutubeChannelsDataYoutubechannels"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        youtube_channels = self.youtube_channels.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "youtubeChannels": youtube_channels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.collect_youtube_channels_data_youtubechannels import CollectYoutubeChannelsDataYoutubechannels

        d = dict(src_dict)
        youtube_channels = CollectYoutubeChannelsDataYoutubechannels.from_dict(d.pop("youtubeChannels"))

        collect_youtube_channels_data = cls(
            youtube_channels=youtube_channels,
        )

        collect_youtube_channels_data.additional_properties = d
        return collect_youtube_channels_data

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
