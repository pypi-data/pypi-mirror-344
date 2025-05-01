from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SerpSchema")


@_attrs_define
class SerpSchema:
    """
    Attributes:
        title (str):
        link (str):
        channel_link (str):
        position_on_page (int):
        published_date (Union[None, Unset, str]):
        id (Union[Unset, UUID]):
    """

    title: str
    link: str
    channel_link: str
    position_on_page: int
    published_date: Union[None, Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        link = self.link

        channel_link = self.channel_link

        position_on_page = self.position_on_page

        published_date: Union[None, Unset, str]
        if isinstance(self.published_date, Unset):
            published_date = UNSET
        else:
            published_date = self.published_date

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "link": link,
                "channelLink": channel_link,
                "positionOnPage": position_on_page,
            }
        )
        if published_date is not UNSET:
            field_dict["publishedDate"] = published_date
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        link = d.pop("link")

        channel_link = d.pop("channelLink")

        position_on_page = d.pop("positionOnPage")

        def _parse_published_date(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        published_date = _parse_published_date(d.pop("publishedDate", UNSET))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        serp_schema = cls(
            title=title,
            link=link,
            channel_link=channel_link,
            position_on_page=position_on_page,
            published_date=published_date,
            id=id,
        )

        serp_schema.additional_properties = d
        return serp_schema

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
