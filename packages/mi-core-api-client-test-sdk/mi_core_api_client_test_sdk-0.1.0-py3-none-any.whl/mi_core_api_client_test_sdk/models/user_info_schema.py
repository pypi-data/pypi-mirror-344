from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_permission import UserPermission
from ..models.user_role import UserRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserInfoSchema")


@_attrs_define
class UserInfoSchema:
    """
    Attributes:
        id (UUID):
        email (str):
        balance (str):
        role (Union[Unset, UserRole]): Enumeration class representing user roles.
        permissions (Union[Unset, list[UserPermission]]):
        api_key_id (Union[None, UUID, Unset]):
    """

    id: UUID
    email: str
    balance: str
    role: Union[Unset, UserRole] = UNSET
    permissions: Union[Unset, list[UserPermission]] = UNSET
    api_key_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        email = self.email

        balance = self.balance

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        permissions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.value
                permissions.append(permissions_item)

        api_key_id: Union[None, Unset, str]
        if isinstance(self.api_key_id, Unset):
            api_key_id = UNSET
        elif isinstance(self.api_key_id, UUID):
            api_key_id = str(self.api_key_id)
        else:
            api_key_id = self.api_key_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "email": email,
                "balance": balance,
            }
        )
        if role is not UNSET:
            field_dict["role"] = role
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if api_key_id is not UNSET:
            field_dict["apiKeyId"] = api_key_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        email = d.pop("email")

        balance = d.pop("balance")

        _role = d.pop("role", UNSET)
        role: Union[Unset, UserRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = UserRole(_role)

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = UserPermission(permissions_item_data)

            permissions.append(permissions_item)

        def _parse_api_key_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                api_key_id_type_0 = UUID(data)

                return api_key_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        api_key_id = _parse_api_key_id(d.pop("apiKeyId", UNSET))

        user_info_schema = cls(
            id=id,
            email=email,
            balance=balance,
            role=role,
            permissions=permissions,
            api_key_id=api_key_id,
        )

        user_info_schema.additional_properties = d
        return user_info_schema

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
