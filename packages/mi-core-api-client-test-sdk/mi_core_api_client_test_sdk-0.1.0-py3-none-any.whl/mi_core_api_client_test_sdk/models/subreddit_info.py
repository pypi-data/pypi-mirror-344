from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubredditInfo")


@_attrs_define
class SubredditInfo:
    """
    Attributes:
        url (str):
        name (str):
        description (str):
        members (int):
        online_members (int):
        thumbnail (str):
        rank (Union[None, Unset, str]):
    """

    url: str
    name: str
    description: str
    members: int
    online_members: int
    thumbnail: str
    rank: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        name = self.name

        description = self.description

        members = self.members

        online_members = self.online_members

        thumbnail = self.thumbnail

        rank: Union[None, Unset, str]
        if isinstance(self.rank, Unset):
            rank = UNSET
        else:
            rank = self.rank

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "name": name,
                "description": description,
                "members": members,
                "onlineMembers": online_members,
                "thumbnail": thumbnail,
            }
        )
        if rank is not UNSET:
            field_dict["rank"] = rank

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        name = d.pop("name")

        description = d.pop("description")

        members = d.pop("members")

        online_members = d.pop("onlineMembers")

        thumbnail = d.pop("thumbnail")

        def _parse_rank(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rank = _parse_rank(d.pop("rank", UNSET))

        subreddit_info = cls(
            url=url,
            name=name,
            description=description,
            members=members,
            online_members=online_members,
            thumbnail=thumbnail,
            rank=rank,
        )

        subreddit_info.additional_properties = d
        return subreddit_info

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
