from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GoogleRawSerpResultDTO")


@_attrs_define
class GoogleRawSerpResultDTO:
    """Raw search result from Google SERP API

    Attributes:
        title (str):
        link (str):
        displayed_link (Union[None, Unset, str]):
        snippet (Union[None, Unset, str]):
        duration (Union[None, Unset, str]):
        source (Union[None, Unset, str]):
    """

    title: str
    link: str
    displayed_link: Union[None, Unset, str] = UNSET
    snippet: Union[None, Unset, str] = UNSET
    duration: Union[None, Unset, str] = UNSET
    source: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        link = self.link

        displayed_link: Union[None, Unset, str]
        if isinstance(self.displayed_link, Unset):
            displayed_link = UNSET
        else:
            displayed_link = self.displayed_link

        snippet: Union[None, Unset, str]
        if isinstance(self.snippet, Unset):
            snippet = UNSET
        else:
            snippet = self.snippet

        duration: Union[None, Unset, str]
        if isinstance(self.duration, Unset):
            duration = UNSET
        else:
            duration = self.duration

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "link": link,
            }
        )
        if displayed_link is not UNSET:
            field_dict["displayedLink"] = displayed_link
        if snippet is not UNSET:
            field_dict["snippet"] = snippet
        if duration is not UNSET:
            field_dict["duration"] = duration
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        link = d.pop("link")

        def _parse_displayed_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        displayed_link = _parse_displayed_link(d.pop("displayedLink", UNSET))

        def _parse_snippet(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        snippet = _parse_snippet(d.pop("snippet", UNSET))

        def _parse_duration(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        duration = _parse_duration(d.pop("duration", UNSET))

        def _parse_source(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source = _parse_source(d.pop("source", UNSET))

        google_raw_serp_result_dto = cls(
            title=title,
            link=link,
            displayed_link=displayed_link,
            snippet=snippet,
            duration=duration,
            source=source,
        )

        google_raw_serp_result_dto.additional_properties = d
        return google_raw_serp_result_dto

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
