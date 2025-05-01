from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.storyboards_by_channel import StoryboardsByChannel


T = TypeVar("T", bound="StoryboardRestrictionsRequest")


@_attrs_define
class StoryboardRestrictionsRequest:
    """
    Attributes:
        youtube_channels (list['StoryboardsByChannel']):
        prompt_id (Union[None, UUID, Unset]):
    """

    youtube_channels: list["StoryboardsByChannel"]
    prompt_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        youtube_channels = []
        for youtube_channels_item_data in self.youtube_channels:
            youtube_channels_item = youtube_channels_item_data.to_dict()
            youtube_channels.append(youtube_channels_item)

        prompt_id: Union[None, Unset, str]
        if isinstance(self.prompt_id, Unset):
            prompt_id = UNSET
        elif isinstance(self.prompt_id, UUID):
            prompt_id = str(self.prompt_id)
        else:
            prompt_id = self.prompt_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "youtube_channels": youtube_channels,
            }
        )
        if prompt_id is not UNSET:
            field_dict["prompt_id"] = prompt_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storyboards_by_channel import StoryboardsByChannel

        d = dict(src_dict)
        youtube_channels = []
        _youtube_channels = d.pop("youtube_channels")
        for youtube_channels_item_data in _youtube_channels:
            youtube_channels_item = StoryboardsByChannel.from_dict(youtube_channels_item_data)

            youtube_channels.append(youtube_channels_item)

        def _parse_prompt_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                prompt_id_type_0 = UUID(data)

                return prompt_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        prompt_id = _parse_prompt_id(d.pop("prompt_id", UNSET))

        storyboard_restrictions_request = cls(
            youtube_channels=youtube_channels,
            prompt_id=prompt_id,
        )

        storyboard_restrictions_request.additional_properties = d
        return storyboard_restrictions_request

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
