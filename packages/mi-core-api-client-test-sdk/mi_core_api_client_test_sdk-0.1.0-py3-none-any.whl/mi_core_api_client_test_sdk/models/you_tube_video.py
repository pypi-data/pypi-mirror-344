import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="YouTubeVideo")


@_attrs_define
class YouTubeVideo:
    """
    Attributes:
        title (str):
        url (str):
        views (int):
        likes (int):
        channel_name (str):
        thumbnail_url (str):
        published_date (datetime.datetime):
    """

    title: str
    url: str
    views: int
    likes: int
    channel_name: str
    thumbnail_url: str
    published_date: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        url = self.url

        views = self.views

        likes = self.likes

        channel_name = self.channel_name

        thumbnail_url = self.thumbnail_url

        published_date = self.published_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "url": url,
                "views": views,
                "likes": likes,
                "channelName": channel_name,
                "thumbnailUrl": thumbnail_url,
                "publishedDate": published_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        url = d.pop("url")

        views = d.pop("views")

        likes = d.pop("likes")

        channel_name = d.pop("channelName")

        thumbnail_url = d.pop("thumbnailUrl")

        published_date = isoparse(d.pop("publishedDate"))

        you_tube_video = cls(
            title=title,
            url=url,
            views=views,
            likes=likes,
            channel_name=channel_name,
            thumbnail_url=thumbnail_url,
            published_date=published_date,
        )

        you_tube_video.additional_properties = d
        return you_tube_video

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
