from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.one_token_schema import OneTokenSchema
    from ..models.password_schema import PasswordSchema


T = TypeVar("T", bound="BodyPasswordResetEmailConfirmAuthPasswordResetConfirmPost")


@_attrs_define
class BodyPasswordResetEmailConfirmAuthPasswordResetConfirmPost:
    """
    Attributes:
        password (PasswordSchema):
        token (OneTokenSchema):
    """

    password: "PasswordSchema"
    token: "OneTokenSchema"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        password = self.password.to_dict()

        token = self.token.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "password": password,
                "token": token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.one_token_schema import OneTokenSchema
        from ..models.password_schema import PasswordSchema

        d = dict(src_dict)
        password = PasswordSchema.from_dict(d.pop("password"))

        token = OneTokenSchema.from_dict(d.pop("token"))

        body_password_reset_email_confirm_auth_password_reset_confirm_post = cls(
            password=password,
            token=token,
        )

        body_password_reset_email_confirm_auth_password_reset_confirm_post.additional_properties = d
        return body_password_reset_email_confirm_auth_password_reset_confirm_post

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
