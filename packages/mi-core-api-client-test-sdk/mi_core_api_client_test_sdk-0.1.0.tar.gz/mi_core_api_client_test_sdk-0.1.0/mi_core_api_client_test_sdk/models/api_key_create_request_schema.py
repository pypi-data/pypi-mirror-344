import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="APIKeyCreateRequestSchema")


@_attrs_define
class APIKeyCreateRequestSchema:
    """
    Attributes:
        expiry_date (datetime.datetime): Expiry date of the API key without timezone
        name (Union[Unset, str]): Name of the API key. Defaults to 'API_KEY' if not provided. Default: 'API_KEY'.
    """

    expiry_date: datetime.datetime
    name: Union[Unset, str] = "API_KEY"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expiry_date = self.expiry_date.isoformat()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expiryDate": expiry_date,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expiry_date = isoparse(d.pop("expiryDate"))

        name = d.pop("name", UNSET)

        api_key_create_request_schema = cls(
            expiry_date=expiry_date,
            name=name,
        )

        api_key_create_request_schema.additional_properties = d
        return api_key_create_request_schema

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
