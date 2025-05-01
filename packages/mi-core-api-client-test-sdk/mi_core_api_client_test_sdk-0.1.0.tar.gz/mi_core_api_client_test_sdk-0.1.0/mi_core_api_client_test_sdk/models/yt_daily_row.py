from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="YTDailyRow")


@_attrs_define
class YTDailyRow:
    """
    Attributes:
        timestamp (str):
        total_views (int):
        subscribers (int):
        views_rank (int):
        subs_rank (int):
    """

    timestamp: str
    total_views: int
    subscribers: int
    views_rank: int
    subs_rank: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp

        total_views = self.total_views

        subscribers = self.subscribers

        views_rank = self.views_rank

        subs_rank = self.subs_rank

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "totalViews": total_views,
                "subscribers": subscribers,
                "viewsRank": views_rank,
                "subsRank": subs_rank,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = d.pop("timestamp")

        total_views = d.pop("totalViews")

        subscribers = d.pop("subscribers")

        views_rank = d.pop("viewsRank")

        subs_rank = d.pop("subsRank")

        yt_daily_row = cls(
            timestamp=timestamp,
            total_views=total_views,
            subscribers=subscribers,
            views_rank=views_rank,
            subs_rank=subs_rank,
        )

        yt_daily_row.additional_properties = d
        return yt_daily_row

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
