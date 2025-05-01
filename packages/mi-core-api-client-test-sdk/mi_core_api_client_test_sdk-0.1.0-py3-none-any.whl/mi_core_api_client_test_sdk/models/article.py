import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Article")


@_attrs_define
class Article:
    """
    Attributes:
        url (Union[None, str]):
        title (Union[None, str]):
        body (Union[None, str]):
        author (Union[None, str]):
        description (Union[None, str]):
        published_date (Union[None, datetime.date]):
        site_name (Union[None, str]):
        image (Union[None, str]):
        categories (list[str]):
        tags (list[str]):
        comments (Union[None, str]):
    """

    url: Union[None, str]
    title: Union[None, str]
    body: Union[None, str]
    author: Union[None, str]
    description: Union[None, str]
    published_date: Union[None, datetime.date]
    site_name: Union[None, str]
    image: Union[None, str]
    categories: list[str]
    tags: list[str]
    comments: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url: Union[None, str]
        url = self.url

        title: Union[None, str]
        title = self.title

        body: Union[None, str]
        body = self.body

        author: Union[None, str]
        author = self.author

        description: Union[None, str]
        description = self.description

        published_date: Union[None, str]
        if isinstance(self.published_date, datetime.date):
            published_date = self.published_date.isoformat()
        else:
            published_date = self.published_date

        site_name: Union[None, str]
        site_name = self.site_name

        image: Union[None, str]
        image = self.image

        categories = self.categories

        tags = self.tags

        comments: Union[None, str]
        comments = self.comments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "title": title,
                "body": body,
                "author": author,
                "description": description,
                "publishedDate": published_date,
                "siteName": site_name,
                "image": image,
                "categories": categories,
                "tags": tags,
                "comments": comments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        def _parse_body(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        body = _parse_body(d.pop("body"))

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

        def _parse_published_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                published_date_type_0 = isoparse(data).date()

                return published_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        published_date = _parse_published_date(d.pop("publishedDate"))

        def _parse_site_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        site_name = _parse_site_name(d.pop("siteName"))

        def _parse_image(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        image = _parse_image(d.pop("image"))

        categories = cast(list[str], d.pop("categories"))

        tags = cast(list[str], d.pop("tags"))

        def _parse_comments(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        comments = _parse_comments(d.pop("comments"))

        article = cls(
            url=url,
            title=title,
            body=body,
            author=author,
            description=description,
            published_date=published_date,
            site_name=site_name,
            image=image,
            categories=categories,
            tags=tags,
            comments=comments,
        )

        article.additional_properties = d
        return article

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
