import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="YoutubeVideoSchema")


@_attrs_define
class YoutubeVideoSchema:
    """
    Attributes:
        url (str):
        title (str):
        published_date (datetime.date):
        views (int):
        likes (int):
        length (str):
        channel_name (str):
        channel_link (str):
        comments_count (int):
        thumbnail_url (str):
        category (str):
        language (str):
        body (Union[None, str]):
        topic_id (UUID):
        is_available (Union[Unset, bool]):  Default: True.
        id (Union[Unset, UUID]):
        updated_at (Union[Unset, datetime.datetime]):  Default: isoparse('2025-05-01T06:12:12.440922Z').
        channel_id (Union[None, UUID, Unset]):
    """

    url: str
    title: str
    published_date: datetime.date
    views: int
    likes: int
    length: str
    channel_name: str
    channel_link: str
    comments_count: int
    thumbnail_url: str
    category: str
    language: str
    body: Union[None, str]
    topic_id: UUID
    is_available: Union[Unset, bool] = True
    id: Union[Unset, UUID] = UNSET
    updated_at: Union[Unset, datetime.datetime] = isoparse("2025-05-01T06:12:12.440922Z")
    channel_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        title = self.title

        published_date = self.published_date.isoformat()

        views = self.views

        likes = self.likes

        length = self.length

        channel_name = self.channel_name

        channel_link = self.channel_link

        comments_count = self.comments_count

        thumbnail_url = self.thumbnail_url

        category = self.category

        language = self.language

        body: Union[None, str]
        body = self.body

        topic_id = str(self.topic_id)

        is_available = self.is_available

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        channel_id: Union[None, Unset, str]
        if isinstance(self.channel_id, Unset):
            channel_id = UNSET
        elif isinstance(self.channel_id, UUID):
            channel_id = str(self.channel_id)
        else:
            channel_id = self.channel_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "title": title,
                "publishedDate": published_date,
                "views": views,
                "likes": likes,
                "length": length,
                "channelName": channel_name,
                "channelLink": channel_link,
                "commentsCount": comments_count,
                "thumbnailUrl": thumbnail_url,
                "category": category,
                "language": language,
                "body": body,
                "topicId": topic_id,
            }
        )
        if is_available is not UNSET:
            field_dict["isAvailable"] = is_available
        if id is not UNSET:
            field_dict["id"] = id
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if channel_id is not UNSET:
            field_dict["channelId"] = channel_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        title = d.pop("title")

        published_date = isoparse(d.pop("publishedDate")).date()

        views = d.pop("views")

        likes = d.pop("likes")

        length = d.pop("length")

        channel_name = d.pop("channelName")

        channel_link = d.pop("channelLink")

        comments_count = d.pop("commentsCount")

        thumbnail_url = d.pop("thumbnailUrl")

        category = d.pop("category")

        language = d.pop("language")

        def _parse_body(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        body = _parse_body(d.pop("body"))

        topic_id = UUID(d.pop("topicId"))

        is_available = d.pop("isAvailable", UNSET)

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

        def _parse_channel_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                channel_id_type_0 = UUID(data)

                return channel_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        channel_id = _parse_channel_id(d.pop("channelId", UNSET))

        youtube_video_schema = cls(
            url=url,
            title=title,
            published_date=published_date,
            views=views,
            likes=likes,
            length=length,
            channel_name=channel_name,
            channel_link=channel_link,
            comments_count=comments_count,
            thumbnail_url=thumbnail_url,
            category=category,
            language=language,
            body=body,
            topic_id=topic_id,
            is_available=is_available,
            id=id,
            updated_at=updated_at,
            channel_id=channel_id,
        )

        youtube_video_schema.additional_properties = d
        return youtube_video_schema

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
