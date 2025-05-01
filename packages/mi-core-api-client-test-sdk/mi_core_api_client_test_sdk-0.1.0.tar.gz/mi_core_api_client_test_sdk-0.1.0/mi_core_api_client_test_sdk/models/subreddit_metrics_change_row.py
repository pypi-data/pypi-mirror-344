from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SubredditMetricsChangeRow")


@_attrs_define
class SubredditMetricsChangeRow:
    """
    Attributes:
        month_year (str):
        members (int):
        global_rank_by_members (int):
    """

    month_year: str
    members: int
    global_rank_by_members: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month_year = self.month_year

        members = self.members

        global_rank_by_members = self.global_rank_by_members

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "monthYear": month_year,
                "members": members,
                "globalRankByMembers": global_rank_by_members,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month_year = d.pop("monthYear")

        members = d.pop("members")

        global_rank_by_members = d.pop("globalRankByMembers")

        subreddit_metrics_change_row = cls(
            month_year=month_year,
            members=members,
            global_rank_by_members=global_rank_by_members,
        )

        subreddit_metrics_change_row.additional_properties = d
        return subreddit_metrics_change_row

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
