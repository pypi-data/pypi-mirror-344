from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InviteCodeSchema")


@_attrs_define
class InviteCodeSchema:
    """
    Attributes:
        code (str):
        storyboard_id (Union[None, UUID, Unset]):
    """

    code: str
    storyboard_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        storyboard_id: Union[None, Unset, str]
        if isinstance(self.storyboard_id, Unset):
            storyboard_id = UNSET
        elif isinstance(self.storyboard_id, UUID):
            storyboard_id = str(self.storyboard_id)
        else:
            storyboard_id = self.storyboard_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
            }
        )
        if storyboard_id is not UNSET:
            field_dict["storyboard_id"] = storyboard_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        def _parse_storyboard_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                storyboard_id_type_0 = UUID(data)

                return storyboard_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        storyboard_id = _parse_storyboard_id(d.pop("storyboard_id", UNSET))

        invite_code_schema = cls(
            code=code,
            storyboard_id=storyboard_id,
        )

        invite_code_schema.additional_properties = d
        return invite_code_schema

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
