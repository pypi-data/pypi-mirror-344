import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sort_options import SortOptions
from ..models.time_filter import TimeFilter
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubRedditParamsDTO")


@_attrs_define
class SubRedditParamsDTO:
    """
    Attributes:
        post_timestamp (datetime.datetime):
        total_posts (int):
        sort_by (SortOptions):
        time_filter (TimeFilter):
        max_duration_sec (Union[Unset, int]):  Default: 60.
    """

    post_timestamp: datetime.datetime
    total_posts: int
    sort_by: SortOptions
    time_filter: TimeFilter
    max_duration_sec: Union[Unset, int] = 60
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        post_timestamp = self.post_timestamp.isoformat()

        total_posts = self.total_posts

        sort_by = self.sort_by.value

        time_filter = self.time_filter.value

        max_duration_sec = self.max_duration_sec

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "postTimestamp": post_timestamp,
                "totalPosts": total_posts,
                "sortBy": sort_by,
                "timeFilter": time_filter,
            }
        )
        if max_duration_sec is not UNSET:
            field_dict["maxDurationSec"] = max_duration_sec

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        post_timestamp = isoparse(d.pop("postTimestamp"))

        total_posts = d.pop("totalPosts")

        sort_by = SortOptions(d.pop("sortBy"))

        time_filter = TimeFilter(d.pop("timeFilter"))

        max_duration_sec = d.pop("maxDurationSec", UNSET)

        sub_reddit_params_dto = cls(
            post_timestamp=post_timestamp,
            total_posts=total_posts,
            sort_by=sort_by,
            time_filter=time_filter,
            max_duration_sec=max_duration_sec,
        )

        sub_reddit_params_dto.additional_properties = d
        return sub_reddit_params_dto

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
