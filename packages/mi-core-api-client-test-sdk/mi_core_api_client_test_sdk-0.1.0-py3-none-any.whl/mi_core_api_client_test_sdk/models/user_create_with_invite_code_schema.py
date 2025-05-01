from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserCreateWithInviteCodeSchema")


@_attrs_define
class UserCreateWithInviteCodeSchema:
    """
    Attributes:
        email (str):
        code (str):
        firstname (Union[None, Unset, str]):
        lastname (Union[None, Unset, str]):
        password (Union[Unset, str]):  Default: '1234567$'.
    """

    email: str
    code: str
    firstname: Union[None, Unset, str] = UNSET
    lastname: Union[None, Unset, str] = UNSET
    password: Union[Unset, str] = "1234567$"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        code = self.code

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

        password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "code": code,
            }
        )
        if firstname is not UNSET:
            field_dict["firstname"] = firstname
        if lastname is not UNSET:
            field_dict["lastname"] = lastname
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        code = d.pop("code")

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

        password = d.pop("password", UNSET)

        user_create_with_invite_code_schema = cls(
            email=email,
            code=code,
            firstname=firstname,
            lastname=lastname,
            password=password,
        )

        user_create_with_invite_code_schema.additional_properties = d
        return user_create_with_invite_code_schema

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
