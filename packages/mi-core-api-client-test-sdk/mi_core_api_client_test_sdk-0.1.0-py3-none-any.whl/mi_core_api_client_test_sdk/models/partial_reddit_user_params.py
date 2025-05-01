import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sort_options import SortOptions
from ..models.time_filter import TimeFilter
from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialRedditUserParams")


@_attrs_define
class PartialRedditUserParams:
    """
    Attributes:
        post_timestamp (Union[None, Unset, datetime.datetime]):
        total_posts (Union[None, Unset, int]):
        sort_by (Union[None, SortOptions, Unset]):
        time_filter (Union[None, TimeFilter, Unset]):
    """

    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    total_posts: Union[None, Unset, int] = UNSET
    sort_by: Union[None, SortOptions, Unset] = UNSET
    time_filter: Union[None, TimeFilter, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post_timestamp: Union[None, Unset, str]
        if isinstance(self.post_timestamp, Unset):
            post_timestamp = UNSET
        elif isinstance(self.post_timestamp, datetime.datetime):
            post_timestamp = self.post_timestamp.isoformat()
        else:
            post_timestamp = self.post_timestamp

        total_posts: Union[None, Unset, int]
        if isinstance(self.total_posts, Unset):
            total_posts = UNSET
        else:
            total_posts = self.total_posts

        sort_by: Union[None, Unset, str]
        if isinstance(self.sort_by, Unset):
            sort_by = UNSET
        elif isinstance(self.sort_by, SortOptions):
            sort_by = self.sort_by.value
        else:
            sort_by = self.sort_by

        time_filter: Union[None, Unset, str]
        if isinstance(self.time_filter, Unset):
            time_filter = UNSET
        elif isinstance(self.time_filter, TimeFilter):
            time_filter = self.time_filter.value
        else:
            time_filter = self.time_filter

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if post_timestamp is not UNSET:
            field_dict["post_timestamp"] = post_timestamp
        if total_posts is not UNSET:
            field_dict["total_posts"] = total_posts
        if sort_by is not UNSET:
            field_dict["sort_by"] = sort_by
        if time_filter is not UNSET:
            field_dict["time_filter"] = time_filter

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        post_timestamp = _parse_post_timestamp(d.pop("post_timestamp", UNSET))

        def _parse_total_posts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_posts = _parse_total_posts(d.pop("total_posts", UNSET))

        def _parse_sort_by(data: object) -> Union[None, SortOptions, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                sort_by_type_0 = SortOptions(data)

                return sort_by_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, SortOptions, Unset], data)

        sort_by = _parse_sort_by(d.pop("sort_by", UNSET))

        def _parse_time_filter(data: object) -> Union[None, TimeFilter, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                time_filter_type_0 = TimeFilter(data)

                return time_filter_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TimeFilter, Unset], data)

        time_filter = _parse_time_filter(d.pop("time_filter", UNSET))

        partial_reddit_user_params = cls(
            post_timestamp=post_timestamp,
            total_posts=total_posts,
            sort_by=sort_by,
            time_filter=time_filter,
        )

        partial_reddit_user_params.additional_properties = d
        return partial_reddit_user_params

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
