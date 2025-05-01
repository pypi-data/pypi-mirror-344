from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubredditSchemaDTO")


@_attrs_define
class SubredditSchemaDTO:
    """
    Attributes:
        name (str):
        subscribers (int):
        description (str):
        url (str):
        online_members (int):
        thumbnail (str):
        rank (Union[None, Unset, str]):
        id (Union[Unset, UUID]):
    """

    name: str
    subscribers: int
    description: str
    url: str
    online_members: int
    thumbnail: str
    rank: Union[None, Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        subscribers = self.subscribers

        description = self.description

        url = self.url

        online_members = self.online_members

        thumbnail = self.thumbnail

        rank: Union[None, Unset, str]
        if isinstance(self.rank, Unset):
            rank = UNSET
        else:
            rank = self.rank

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "subscribers": subscribers,
                "description": description,
                "url": url,
                "onlineMembers": online_members,
                "thumbnail": thumbnail,
            }
        )
        if rank is not UNSET:
            field_dict["rank"] = rank
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        subscribers = d.pop("subscribers")

        description = d.pop("description")

        url = d.pop("url")

        online_members = d.pop("onlineMembers")

        thumbnail = d.pop("thumbnail")

        def _parse_rank(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rank = _parse_rank(d.pop("rank", UNSET))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        subreddit_schema_dto = cls(
            name=name,
            subscribers=subscribers,
            description=description,
            url=url,
            online_members=online_members,
            thumbnail=thumbnail,
            rank=rank,
            id=id,
        )

        subreddit_schema_dto.additional_properties = d
        return subreddit_schema_dto

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
