import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="YoutubeChannelParamsDTO")


@_attrs_define
class YoutubeChannelParamsDTO:
    """
    Attributes:
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]):
    """

    with_transcript: Union[Unset, bool] = False
    total_posts: Union[None, Unset, int] = UNSET
    max_duration_sec: Union[Unset, int] = 60
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        with_transcript = self.with_transcript

        total_posts: Union[None, Unset, int]
        if isinstance(self.total_posts, Unset):
            total_posts = UNSET
        else:
            total_posts = self.total_posts

        max_duration_sec = self.max_duration_sec

        post_timestamp: Union[None, Unset, str]
        if isinstance(self.post_timestamp, Unset):
            post_timestamp = UNSET
        elif isinstance(self.post_timestamp, datetime.datetime):
            post_timestamp = self.post_timestamp.isoformat()
        else:
            post_timestamp = self.post_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if with_transcript is not UNSET:
            field_dict["withTranscript"] = with_transcript
        if total_posts is not UNSET:
            field_dict["totalPosts"] = total_posts
        if max_duration_sec is not UNSET:
            field_dict["maxDurationSec"] = max_duration_sec
        if post_timestamp is not UNSET:
            field_dict["postTimestamp"] = post_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        with_transcript = d.pop("withTranscript", UNSET)

        def _parse_total_posts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_posts = _parse_total_posts(d.pop("totalPosts", UNSET))

        max_duration_sec = d.pop("maxDurationSec", UNSET)

        def _parse_post_timestamp(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                post_timestamp_type_0 = isoparse(data)

                return post_timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        post_timestamp = _parse_post_timestamp(d.pop("postTimestamp", UNSET))

        youtube_channel_params_dto = cls(
            with_transcript=with_transcript,
            total_posts=total_posts,
            max_duration_sec=max_duration_sec,
            post_timestamp=post_timestamp,
        )

        youtube_channel_params_dto.additional_properties = d
        return youtube_channel_params_dto

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
