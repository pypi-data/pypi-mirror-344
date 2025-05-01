from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_permission import UserPermission
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUpdateSchema")


@_attrs_define
class UserUpdateSchema:
    """
    Attributes:
        firstname (Union[None, Unset, str]):
        lastname (Union[None, Unset, str]):
        permissions (Union[Unset, list[UserPermission]]):
    """

    firstname: Union[None, Unset, str] = UNSET
    lastname: Union[None, Unset, str] = UNSET
    permissions: Union[Unset, list[UserPermission]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        firstname: Union[None, Unset, str]
        if isinstance(self.firstname, Unset):
            firstname = UNSET
        else:
            firstname = self.firstname

        lastname: Union[None, Unset, str]
        if isinstance(self.lastname, Unset):
            lastname = UNSET
        else:
            lastname = self.lastname

        permissions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.value
                permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if firstname is not UNSET:
            field_dict["firstname"] = firstname
        if lastname is not UNSET:
            field_dict["lastname"] = lastname
        if permissions is not UNSET:
            field_dict["permissions"] = permissions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_firstname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        firstname = _parse_firstname(d.pop("firstname", UNSET))

        def _parse_lastname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        lastname = _parse_lastname(d.pop("lastname", UNSET))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = UserPermission(permissions_item_data)

            permissions.append(permissions_item)

        user_update_schema = cls(
            firstname=firstname,
            lastname=lastname,
            permissions=permissions,
        )

        user_update_schema.additional_properties = d
        return user_update_schema

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
