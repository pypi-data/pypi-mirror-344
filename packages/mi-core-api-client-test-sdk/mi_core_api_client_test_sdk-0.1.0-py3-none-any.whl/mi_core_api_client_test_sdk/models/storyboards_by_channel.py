from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StoryboardsByChannel")


@_attrs_define
class StoryboardsByChannel:
    """
    Attributes:
        id (UUID):
        storyboards (list[UUID]):
    """

    id: UUID
    storyboards: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        storyboards = []
        for storyboards_item_data in self.storyboards:
            storyboards_item = str(storyboards_item_data)
            storyboards.append(storyboards_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "storyboards": storyboards,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        storyboards = []
        _storyboards = d.pop("storyboards")
        for storyboards_item_data in _storyboards:
            storyboards_item = UUID(storyboards_item_data)

            storyboards.append(storyboards_item)

        storyboards_by_channel = cls(
            id=id,
            storyboards=storyboards,
        )

        storyboards_by_channel.additional_properties = d
        return storyboards_by_channel

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
