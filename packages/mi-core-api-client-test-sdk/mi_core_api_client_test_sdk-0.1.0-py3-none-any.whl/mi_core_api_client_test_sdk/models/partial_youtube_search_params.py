from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.youtube_search_duration import YoutubeSearchDuration
from ..models.youtube_search_sort_by import YoutubeSearchSortBy
from ..models.youtube_search_upload_date import YoutubeSearchUploadDate
from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialYoutubeSearchParams")


@_attrs_define
class PartialYoutubeSearchParams:
    """
    Attributes:
        total_posts (Union[None, Unset, int]):
        upload_date (Union[None, Unset, YoutubeSearchUploadDate]):
        sort_by (Union[None, Unset, YoutubeSearchSortBy]):
        duration (Union[None, Unset, YoutubeSearchDuration]):
        with_comments (Union[None, Unset, bool]):
        with_transcript (Union[None, Unset, bool]):
        max_duration_sec (Union[None, Unset, int]):
    """

    total_posts: Union[None, Unset, int] = UNSET
    upload_date: Union[None, Unset, YoutubeSearchUploadDate] = UNSET
    sort_by: Union[None, Unset, YoutubeSearchSortBy] = UNSET
    duration: Union[None, Unset, YoutubeSearchDuration] = UNSET
    with_comments: Union[None, Unset, bool] = UNSET
    with_transcript: Union[None, Unset, bool] = UNSET
    max_duration_sec: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_posts: Union[None, Unset, int]
        if isinstance(self.total_posts, Unset):
            total_posts = UNSET
        else:
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

        with_comments: Union[None, Unset, bool]
        if isinstance(self.with_comments, Unset):
            with_comments = UNSET
        else:
            with_comments = self.with_comments

        with_transcript: Union[None, Unset, bool]
        if isinstance(self.with_transcript, Unset):
            with_transcript = UNSET
        else:
            with_transcript = self.with_transcript

        max_duration_sec: Union[None, Unset, int]
        if isinstance(self.max_duration_sec, Unset):
            max_duration_sec = UNSET
        else:
            max_duration_sec = self.max_duration_sec

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_posts is not UNSET:
            field_dict["total_posts"] = total_posts
        if upload_date is not UNSET:
            field_dict["upload_date"] = upload_date
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by
        if duration is not UNSET:
            field_dict["duration"] = duration
        if with_comments is not UNSET:
            field_dict["with_comments"] = with_comments
        if with_transcript is not UNSET:
            field_dict["with_transcript"] = with_transcript
        if max_duration_sec is not UNSET:
            field_dict["max_duration_sec"] = max_duration_sec

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_total_posts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_posts = _parse_total_posts(d.pop("total_posts", UNSET))

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

        upload_date = _parse_upload_date(d.pop("upload_date", UNSET))

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

        sort_by = _parse_sort_by(d.pop("sort_by", UNSET))

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

        def _parse_with_comments(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        with_comments = _parse_with_comments(d.pop("with_comments", UNSET))

        def _parse_with_transcript(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        with_transcript = _parse_with_transcript(d.pop("with_transcript", UNSET))

        def _parse_max_duration_sec(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_duration_sec = _parse_max_duration_sec(d.pop("max_duration_sec", UNSET))

        partial_youtube_search_params = cls(
            total_posts=total_posts,
            upload_date=upload_date,
            sort_by=sort_by,
            duration=duration,
            with_comments=with_comments,
            with_transcript=with_transcript,
            max_duration_sec=max_duration_sec,
        )

        partial_youtube_search_params.additional_properties = d
        return partial_youtube_search_params

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
