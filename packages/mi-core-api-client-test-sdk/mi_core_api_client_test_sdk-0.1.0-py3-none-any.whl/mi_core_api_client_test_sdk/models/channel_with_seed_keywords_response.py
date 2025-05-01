from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChannelWithSeedKeywordsResponse")


@_attrs_define
class ChannelWithSeedKeywordsResponse:
    """
    Attributes:
        name (str):
        seed_keywords (list[str]):
        storyboards (list[UUID]):
        id (Union[Unset, UUID]):
    """

    name: str
    seed_keywords: list[str]
    storyboards: list[UUID]
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        seed_keywords = self.seed_keywords

        storyboards = []
        for storyboards_item_data in self.storyboards:
            storyboards_item = str(storyboards_item_data)
            storyboards.append(storyboards_item)

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "seedKeywords": seed_keywords,
                "storyboards": storyboards,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        seed_keywords = cast(list[str], d.pop("seedKeywords"))

        storyboards = []
        _storyboards = d.pop("storyboards")
        for storyboards_item_data in _storyboards:
            storyboards_item = UUID(storyboards_item_data)

            storyboards.append(storyboards_item)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        channel_with_seed_keywords_response = cls(
            name=name,
            seed_keywords=seed_keywords,
            storyboards=storyboards,
            id=id,
        )

        channel_with_seed_keywords_response.additional_properties = d
        return channel_with_seed_keywords_response

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
