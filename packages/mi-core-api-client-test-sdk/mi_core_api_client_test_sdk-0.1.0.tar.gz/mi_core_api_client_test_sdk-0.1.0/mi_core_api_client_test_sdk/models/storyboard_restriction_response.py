from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StoryboardRestrictionResponse")


@_attrs_define
class StoryboardRestrictionResponse:
    """
    Attributes:
        hard_restrictions (list[str]):
        id (Union[Unset, UUID]):
        soft_restrictions (Union[None, Unset, list[str]]):
    """

    hard_restrictions: list[str]
    id: Union[Unset, UUID] = UNSET
    soft_restrictions: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hard_restrictions = self.hard_restrictions

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        soft_restrictions: Union[None, Unset, list[str]]
        if isinstance(self.soft_restrictions, Unset):
            soft_restrictions = UNSET
        elif isinstance(self.soft_restrictions, list):
            soft_restrictions = self.soft_restrictions

        else:
            soft_restrictions = self.soft_restrictions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hardRestrictions": hard_restrictions,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if soft_restrictions is not UNSET:
            field_dict["softRestrictions"] = soft_restrictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hard_restrictions = cast(list[str], d.pop("hardRestrictions"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        def _parse_soft_restrictions(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                soft_restrictions_type_0 = cast(list[str], data)

                return soft_restrictions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        soft_restrictions = _parse_soft_restrictions(d.pop("softRestrictions", UNSET))

        storyboard_restriction_response = cls(
            hard_restrictions=hard_restrictions,
            id=id,
            soft_restrictions=soft_restrictions,
        )

        storyboard_restriction_response.additional_properties = d
        return storyboard_restriction_response

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
