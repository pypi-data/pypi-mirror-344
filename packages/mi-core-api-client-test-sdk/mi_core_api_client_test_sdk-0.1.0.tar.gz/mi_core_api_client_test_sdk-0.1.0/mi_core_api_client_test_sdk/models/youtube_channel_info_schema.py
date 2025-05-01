import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="YoutubeChannelInfoSchema")


@_attrs_define
class YoutubeChannelInfoSchema:
    """
    Attributes:
        topic_id (UUID):
        url (str):
        title (str):
        id (Union[Unset, UUID]):
        body (Union[Unset, str]):  Default: ''.
        updated_at (Union[Unset, datetime.datetime]):  Default: isoparse('2025-05-01T06:12:12.440922Z').
        subscribers (Union[Unset, int]):  Default: 0.
        total_views (Union[Unset, int]):  Default: 0.
        total_videos (Union[Unset, int]):  Default: 0.
        country (Union[Unset, str]):  Default: ''.
        channel_logo_url (Union[Unset, str]):  Default: ''.
        registered_date (Union[Unset, datetime.date]):  Default: isoparse('2025-05-01').date().
        language (Union[Unset, str]):  Default: ''.
    """

    topic_id: UUID
    url: str
    title: str
    id: Union[Unset, UUID] = UNSET
    body: Union[Unset, str] = ""
    updated_at: Union[Unset, datetime.datetime] = isoparse("2025-05-01T06:12:12.440922Z")
    subscribers: Union[Unset, int] = 0
    total_views: Union[Unset, int] = 0
    total_videos: Union[Unset, int] = 0
    country: Union[Unset, str] = ""
    channel_logo_url: Union[Unset, str] = ""
    registered_date: Union[Unset, datetime.date] = isoparse("2025-05-01").date()
    language: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        topic_id = str(self.topic_id)

        url = self.url

        title = self.title

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        body = self.body

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        subscribers = self.subscribers

        total_views = self.total_views

        total_videos = self.total_videos

        country = self.country

        channel_logo_url = self.channel_logo_url

        registered_date: Union[Unset, str] = UNSET
        if not isinstance(self.registered_date, Unset):
            registered_date = self.registered_date.isoformat()

        language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topicId": topic_id,
                "url": url,
                "title": title,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if body is not UNSET:
            field_dict["body"] = body
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if subscribers is not UNSET:
            field_dict["subscribers"] = subscribers
        if total_views is not UNSET:
            field_dict["totalViews"] = total_views
        if total_videos is not UNSET:
            field_dict["totalVideos"] = total_videos
        if country is not UNSET:
            field_dict["country"] = country
        if channel_logo_url is not UNSET:
            field_dict["channelLogoUrl"] = channel_logo_url
        if registered_date is not UNSET:
            field_dict["registeredDate"] = registered_date
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        topic_id = UUID(d.pop("topicId"))

        url = d.pop("url")

        title = d.pop("title")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        body = d.pop("body", UNSET)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        subscribers = d.pop("subscribers", UNSET)

        total_views = d.pop("totalViews", UNSET)

        total_videos = d.pop("totalVideos", UNSET)

        country = d.pop("country", UNSET)

        channel_logo_url = d.pop("channelLogoUrl", UNSET)

        _registered_date = d.pop("registeredDate", UNSET)
        registered_date: Union[Unset, datetime.date]
        if isinstance(_registered_date, Unset):
            registered_date = UNSET
        else:
            registered_date = isoparse(_registered_date).date()

        language = d.pop("language", UNSET)

        youtube_channel_info_schema = cls(
            topic_id=topic_id,
            url=url,
            title=title,
            id=id,
            body=body,
            updated_at=updated_at,
            subscribers=subscribers,
            total_views=total_views,
            total_videos=total_videos,
            country=country,
            channel_logo_url=channel_logo_url,
            registered_date=registered_date,
            language=language,
        )

        youtube_channel_info_schema.additional_properties = d
        return youtube_channel_info_schema

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
