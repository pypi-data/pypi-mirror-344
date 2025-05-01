import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.user_permission import UserPermission
from ..types import UNSET, Unset

T = TypeVar("T", bound="APIKeyDTO")


@_attrs_define
class APIKeyDTO:
    """
    Attributes:
        id (UUID):
        expiry_date (datetime.datetime):
        permissions (list[UserPermission]):
        name (Union[Unset, str]): Name of the API key. Defaults to 'API_KEY' if not provided. Default: 'API_KEY'.
        api_key (Union[None, Unset, str]):
    """

    id: UUID
    expiry_date: datetime.datetime
    permissions: list[UserPermission]
    name: Union[Unset, str] = "API_KEY"
    api_key: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        expiry_date = self.expiry_date.isoformat()

        permissions = []
        for permissions_item_data in self.permissions:
            permissions_item = permissions_item_data.value
            permissions.append(permissions_item)

        name = self.name

        api_key: Union[None, Unset, str]
        if isinstance(self.api_key, Unset):
            api_key = UNSET
        else:
            api_key = self.api_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "expiryDate": expiry_date,
                "permissions": permissions,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if api_key is not UNSET:
            field_dict["apiKey"] = api_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        expiry_date = isoparse(d.pop("expiryDate"))

        permissions = []
        _permissions = d.pop("permissions")
        for permissions_item_data in _permissions:
            permissions_item = UserPermission(permissions_item_data)

            permissions.append(permissions_item)

        name = d.pop("name", UNSET)

        def _parse_api_key(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_key = _parse_api_key(d.pop("apiKey", UNSET))

        api_key_dto = cls(
            id=id,
            expiry_date=expiry_date,
            permissions=permissions,
            name=name,
            api_key=api_key,
        )

        api_key_dto.additional_properties = d
        return api_key_dto

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
