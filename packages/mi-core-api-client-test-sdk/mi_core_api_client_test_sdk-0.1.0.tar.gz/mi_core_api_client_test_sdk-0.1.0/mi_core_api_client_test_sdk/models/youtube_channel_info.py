from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="YoutubeChannelInfo")


@_attrs_define
class YoutubeChannelInfo:
    """
    Attributes:
        channel_name (str):
        description (str):
        url (str):
        subscriber_count (int):
        total_views (int):
        video_count (int):
        country (Union[None, str]):
        channel_logo_url (Union[None, str]):
        registered_date (Union[None, str]):
    """

    channel_name: str
    description: str
    url: str
    subscriber_count: int
    total_views: int
    video_count: int
    country: Union[None, str]
    channel_logo_url: Union[None, str]
    registered_date: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel_name = self.channel_name

        description = self.description

        url = self.url

        subscriber_count = self.subscriber_count

        total_views = self.total_views

        video_count = self.video_count

        country: Union[None, str]
        country = self.country

        channel_logo_url: Union[None, str]
        channel_logo_url = self.channel_logo_url

        registered_date: Union[None, str]
        registered_date = self.registered_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channelName": channel_name,
                "description": description,
                "url": url,
                "subscriberCount": subscriber_count,
                "totalViews": total_views,
                "videoCount": video_count,
                "country": country,
                "channelLogoUrl": channel_logo_url,
                "registeredDate": registered_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel_name = d.pop("channelName")

        description = d.pop("description")

        url = d.pop("url")

        subscriber_count = d.pop("subscriberCount")

        total_views = d.pop("totalViews")

        video_count = d.pop("videoCount")

        def _parse_country(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        country = _parse_country(d.pop("country"))

        def _parse_channel_logo_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        channel_logo_url = _parse_channel_logo_url(d.pop("channelLogoUrl"))

        def _parse_registered_date(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        registered_date = _parse_registered_date(d.pop("registeredDate"))

        youtube_channel_info = cls(
            channel_name=channel_name,
            description=description,
            url=url,
            subscriber_count=subscriber_count,
            total_views=total_views,
            video_count=video_count,
            country=country,
            channel_logo_url=channel_logo_url,
            registered_date=registered_date,
        )

        youtube_channel_info.additional_properties = d
        return youtube_channel_info

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
