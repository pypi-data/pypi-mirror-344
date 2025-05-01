from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.channel_with_seed_keywords_response import ChannelWithSeedKeywordsResponse


T = TypeVar("T", bound="StoryboardSeedKeywordsResponse")


@_attrs_define
class StoryboardSeedKeywordsResponse:
    """
    Attributes:
        youtube_channels (list['ChannelWithSeedKeywordsResponse']):
    """

    youtube_channels: list["ChannelWithSeedKeywordsResponse"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        youtube_channels = []
        for youtube_channels_item_data in self.youtube_channels:
            youtube_channels_item = youtube_channels_item_data.to_dict()
            youtube_channels.append(youtube_channels_item)

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
        from ..models.channel_with_seed_keywords_response import ChannelWithSeedKeywordsResponse

        d = dict(src_dict)
        youtube_channels = []
        _youtube_channels = d.pop("youtubeChannels")
        for youtube_channels_item_data in _youtube_channels:
            youtube_channels_item = ChannelWithSeedKeywordsResponse.from_dict(youtube_channels_item_data)

            youtube_channels.append(youtube_channels_item)

        storyboard_seed_keywords_response = cls(
            youtube_channels=youtube_channels,
        )

        storyboard_seed_keywords_response.additional_properties = d
        return storyboard_seed_keywords_response

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
