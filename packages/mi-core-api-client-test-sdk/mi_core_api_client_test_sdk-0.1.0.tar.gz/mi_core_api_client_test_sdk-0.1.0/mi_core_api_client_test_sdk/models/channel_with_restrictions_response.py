from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.storyboard_restriction_response import StoryboardRestrictionResponse


T = TypeVar("T", bound="ChannelWithRestrictionsResponse")


@_attrs_define
class ChannelWithRestrictionsResponse:
    """
    Attributes:
        name (str):
        storyboards (list['StoryboardRestrictionResponse']):
        id (Union[Unset, UUID]):
    """

    name: str
    storyboards: list["StoryboardRestrictionResponse"]
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        storyboards = []
        for storyboards_item_data in self.storyboards:
            storyboards_item = storyboards_item_data.to_dict()
            storyboards.append(storyboards_item)

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "storyboards": storyboards,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storyboard_restriction_response import StoryboardRestrictionResponse

        d = dict(src_dict)
        name = d.pop("name")

        storyboards = []
        _storyboards = d.pop("storyboards")
        for storyboards_item_data in _storyboards:
            storyboards_item = StoryboardRestrictionResponse.from_dict(storyboards_item_data)

            storyboards.append(storyboards_item)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        channel_with_restrictions_response = cls(
            name=name,
            storyboards=storyboards,
            id=id,
        )

        channel_with_restrictions_response.additional_properties = d
        return channel_with_restrictions_response

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
