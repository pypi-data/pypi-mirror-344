from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.youtube_search_duration import YoutubeSearchDuration
from ..models.youtube_search_sort_by import YoutubeSearchSortBy
from ..models.youtube_search_upload_date import YoutubeSearchUploadDate
from ..types import UNSET, Unset

T = TypeVar("T", bound="YoutubeSearchParamsDTO")


@_attrs_define
class YoutubeSearchParamsDTO:
    """
    Attributes:
        total_posts (int):
        upload_date (Union[None, Unset, YoutubeSearchUploadDate]):
        sort_by (Union[None, Unset, YoutubeSearchSortBy]):
        duration (Union[None, Unset, YoutubeSearchDuration]):
        with_comments (Union[Unset, bool]):  Default: False.
        with_transcript (Union[Unset, bool]):  Default: False.
        max_duration_sec (Union[None, Unset, int]):
    """

    total_posts: int
    upload_date: Union[None, Unset, YoutubeSearchUploadDate] = UNSET
    sort_by: Union[None, Unset, YoutubeSearchSortBy] = UNSET
    duration: Union[None, Unset, YoutubeSearchDuration] = UNSET
    with_comments: Union[Unset, bool] = False
    with_transcript: Union[Unset, bool] = False
    max_duration_sec: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_posts = self.total_posts

        upload_date: Union[None, Unset, str]
        if isinstance(self.upload_date, Unset):
            upload_date = UNSET
        elif isinstance(self.upload_date, YoutubeSearchUploadDate):
            upload_date = self.upload_date.value
        else:
            upload_date = self.upload_date

        sort_by: Union[None, Unset, str]
        if isinstance(self.sort_by, Unset):
            sort_by = UNSET
        elif isinstance(self.sort_by, YoutubeSearchSortBy):
            sort_by = self.sort_by.value
        else:
            sort_by = self.sort_by

        duration: Union[None, Unset, str]
        if isinstance(self.duration, Unset):
            duration = UNSET
        elif isinstance(self.duration, YoutubeSearchDuration):
            duration = self.duration.value
        else:
            duration = self.duration

        with_comments = self.with_comments

        with_transcript = self.with_transcript

        max_duration_sec: Union[None, Unset, int]
        if isinstance(self.max_duration_sec, Unset):
            max_duration_sec = UNSET
        else:
            max_duration_sec = self.max_duration_sec

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "totalPosts": total_posts,
            }
        )
        if upload_date is not UNSET:
            field_dict["uploadDate"] = upload_date
        if sort_by is not UNSET:
            field_dict["sortBy"] = sort_by
        if duration is not UNSET:
            field_dict["duration"] = duration
        if with_comments is not UNSET:
            field_dict["withComments"] = with_comments
        if with_transcript is not UNSET:
            field_dict["withTranscript"] = with_transcript
        if max_duration_sec is not UNSET:
            field_dict["maxDurationSec"] = max_duration_sec

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_posts = d.pop("totalPosts")

        def _parse_upload_date(data: object) -> Union[None, Unset, YoutubeSearchUploadDate]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                upload_date_type_0 = YoutubeSearchUploadDate(data)

                return upload_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, YoutubeSearchUploadDate], data)

        upload_date = _parse_upload_date(d.pop("uploadDate", UNSET))

        def _parse_sort_by(data: object) -> Union[None, Unset, YoutubeSearchSortBy]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                sort_by_type_0 = YoutubeSearchSortBy(data)

                return sort_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, YoutubeSearchSortBy], data)

        sort_by = _parse_sort_by(d.pop("sortBy", UNSET))

        def _parse_duration(data: object) -> Union[None, Unset, YoutubeSearchDuration]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                duration_type_0 = YoutubeSearchDuration(data)

                return duration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, YoutubeSearchDuration], data)

        duration = _parse_duration(d.pop("duration", UNSET))

        with_comments = d.pop("withComments", UNSET)

        with_transcript = d.pop("withTranscript", UNSET)

        def _parse_max_duration_sec(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_duration_sec = _parse_max_duration_sec(d.pop("maxDurationSec", UNSET))

        youtube_search_params_dto = cls(
            total_posts=total_posts,
            upload_date=upload_date,
            sort_by=sort_by,
            duration=duration,
            with_comments=with_comments,
            with_transcript=with_transcript,
            max_duration_sec=max_duration_sec,
        )

        youtube_search_params_dto.additional_properties = d
        return youtube_search_params_dto

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
