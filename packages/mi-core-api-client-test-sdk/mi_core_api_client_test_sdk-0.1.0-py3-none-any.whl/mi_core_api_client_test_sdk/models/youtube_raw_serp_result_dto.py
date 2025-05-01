from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.raw_serp_channel_result_dto import RawSerpChannelResultDTO


T = TypeVar("T", bound="YoutubeRawSerpResultDTO")


@_attrs_define
class YoutubeRawSerpResultDTO:
    """Raw search result from YouTube SERP API

    Attributes:
        title (str):
        link (str):
        channel (RawSerpChannelResultDTO):
        published_date (Union[None, Unset, str]):
        views (Union[None, Unset, int]):
        length (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
    """

    title: str
    link: str
    channel: "RawSerpChannelResultDTO"
    published_date: Union[None, Unset, str] = UNSET
    views: Union[None, Unset, int] = UNSET
    length: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        link = self.link

        channel = self.channel.to_dict()

        published_date: Union[None, Unset, str]
        if isinstance(self.published_date, Unset):
            published_date = UNSET
        else:
            published_date = self.published_date

        views: Union[None, Unset, int]
        if isinstance(self.views, Unset):
            views = UNSET
        else:
            views = self.views

        length: Union[None, Unset, str]
        if isinstance(self.length, Unset):
            length = UNSET
        else:
            length = self.length

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "link": link,
                "channel": channel,
            }
        )
        if published_date is not UNSET:
            field_dict["publishedDate"] = published_date
        if views is not UNSET:
            field_dict["views"] = views
        if length is not UNSET:
            field_dict["length"] = length
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.raw_serp_channel_result_dto import RawSerpChannelResultDTO

        d = dict(src_dict)
        title = d.pop("title")

        link = d.pop("link")

        channel = RawSerpChannelResultDTO.from_dict(d.pop("channel"))

        def _parse_published_date(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        published_date = _parse_published_date(d.pop("publishedDate", UNSET))

        def _parse_views(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        views = _parse_views(d.pop("views", UNSET))

        def _parse_length(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        length = _parse_length(d.pop("length", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        youtube_raw_serp_result_dto = cls(
            title=title,
            link=link,
            channel=channel,
            published_date=published_date,
            views=views,
            length=length,
            description=description,
        )

        youtube_raw_serp_result_dto.additional_properties = d
        return youtube_raw_serp_result_dto

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
