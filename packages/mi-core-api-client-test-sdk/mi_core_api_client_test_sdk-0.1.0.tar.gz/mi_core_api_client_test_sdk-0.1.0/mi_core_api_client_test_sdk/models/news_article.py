import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="NewsArticle")


@_attrs_define
class NewsArticle:
    """
    Attributes:
        title (str):
        url (str):
        description (str):
        tags (str):
        published_date (datetime.datetime):
    """

    title: str
    url: str
    description: str
    tags: str
    published_date: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        url = self.url

        description = self.description

        tags = self.tags

        published_date = self.published_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "url": url,
                "description": description,
                "tags": tags,
                "publishedDate": published_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        url = d.pop("url")

        description = d.pop("description")

        tags = d.pop("tags")

        published_date = isoparse(d.pop("publishedDate"))

        news_article = cls(
            title=title,
            url=url,
            description=description,
            tags=tags,
            published_date=published_date,
        )

        news_article.additional_properties = d
        return news_article

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
