import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArticleSchema")


@_attrs_define
class ArticleSchema:
    """
    Attributes:
        body (Union[None, str]):
        topic_id (UUID):
        url (Union[None, str]):
        title (Union[None, str]):
        author (Union[None, str]):
        description (Union[None, str]):
        date (datetime.date):
        site_name (Union[None, str]):
        categories (str):
        tags (str):
        language (str):
        id (Union[Unset, UUID]):
        updated_at (Union[Unset, datetime.datetime]):  Default: isoparse('2025-05-01T06:12:12.440922Z').
    """

    body: Union[None, str]
    topic_id: UUID
    url: Union[None, str]
    title: Union[None, str]
    author: Union[None, str]
    description: Union[None, str]
    date: datetime.date
    site_name: Union[None, str]
    categories: str
    tags: str
    language: str
    id: Union[Unset, UUID] = UNSET
    updated_at: Union[Unset, datetime.datetime] = isoparse("2025-05-01T06:12:12.440922Z")
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body: Union[None, str]
        body = self.body

        topic_id = str(self.topic_id)

        url: Union[None, str]
        url = self.url

        title: Union[None, str]
        title = self.title

        author: Union[None, str]
        author = self.author

        description: Union[None, str]
        description = self.description

        date = self.date.isoformat()

        site_name: Union[None, str]
        site_name = self.site_name

        categories = self.categories

        tags = self.tags

        language = self.language

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
                "topicId": topic_id,
                "url": url,
                "title": title,
                "author": author,
                "description": description,
                "date": date,
                "siteName": site_name,
                "categories": categories,
                "tags": tags,
                "language": language,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_body(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        body = _parse_body(d.pop("body"))

        topic_id = UUID(d.pop("topicId"))

        def _parse_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        url = _parse_url(d.pop("url"))

        def _parse_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        title = _parse_title(d.pop("title"))

        def _parse_author(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        author = _parse_author(d.pop("author"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        date = isoparse(d.pop("date")).date()

        def _parse_site_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        site_name = _parse_site_name(d.pop("siteName"))

        categories = d.pop("categories")

        tags = d.pop("tags")

        language = d.pop("language")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        article_schema = cls(
            body=body,
            topic_id=topic_id,
            url=url,
            title=title,
            author=author,
            description=description,
            date=date,
            site_name=site_name,
            categories=categories,
            tags=tags,
            language=language,
            id=id,
            updated_at=updated_at,
        )

        article_schema.additional_properties = d
        return article_schema

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
