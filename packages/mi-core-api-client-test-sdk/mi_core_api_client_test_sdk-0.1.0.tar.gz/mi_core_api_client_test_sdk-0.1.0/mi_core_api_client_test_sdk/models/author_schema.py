from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthorSchema")


@_attrs_define
class AuthorSchema:
    """
    Attributes:
        name (str):
        profile_url (Union[None, Unset, str]):
        post_karma (Union[None, Unset, int]):
        comment_karma (Union[None, Unset, int]):
    """

    name: str
    profile_url: Union[None, Unset, str] = UNSET
    post_karma: Union[None, Unset, int] = UNSET
    comment_karma: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        profile_url: Union[None, Unset, str]
        if isinstance(self.profile_url, Unset):
            profile_url = UNSET
        else:
            profile_url = self.profile_url

        post_karma: Union[None, Unset, int]
        if isinstance(self.post_karma, Unset):
            post_karma = UNSET
        else:
            post_karma = self.post_karma

        comment_karma: Union[None, Unset, int]
        if isinstance(self.comment_karma, Unset):
            comment_karma = UNSET
        else:
            comment_karma = self.comment_karma

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if profile_url is not UNSET:
            field_dict["profileUrl"] = profile_url
        if post_karma is not UNSET:
            field_dict["postKarma"] = post_karma
        if comment_karma is not UNSET:
            field_dict["commentKarma"] = comment_karma

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_profile_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile_url = _parse_profile_url(d.pop("profileUrl", UNSET))

        def _parse_post_karma(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        post_karma = _parse_post_karma(d.pop("postKarma", UNSET))

        def _parse_comment_karma(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        comment_karma = _parse_comment_karma(d.pop("commentKarma", UNSET))

        author_schema = cls(
            name=name,
            profile_url=profile_url,
            post_karma=post_karma,
            comment_karma=comment_karma,
        )

        author_schema.additional_properties = d
        return author_schema

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
