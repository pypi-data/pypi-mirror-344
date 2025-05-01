from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SubredditRankChangeRow")


@_attrs_define
class SubredditRankChangeRow:
    """
    Attributes:
        month_year (str):
        global_rank_change_members (Union[None, int]):
        global_rank_pct_change_members (Union[None, float]):
    """

    month_year: str
    global_rank_change_members: Union[None, int]
    global_rank_pct_change_members: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month_year = self.month_year

        global_rank_change_members: Union[None, int]
        global_rank_change_members = self.global_rank_change_members

        global_rank_pct_change_members: Union[None, float]
        global_rank_pct_change_members = self.global_rank_pct_change_members

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "monthYear": month_year,
                "globalRankChangeMembers": global_rank_change_members,
                "globalRankPctChangeMembers": global_rank_pct_change_members,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month_year = d.pop("monthYear")

        def _parse_global_rank_change_members(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        global_rank_change_members = _parse_global_rank_change_members(d.pop("globalRankChangeMembers"))

        def _parse_global_rank_pct_change_members(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        global_rank_pct_change_members = _parse_global_rank_pct_change_members(d.pop("globalRankPctChangeMembers"))

        subreddit_rank_change_row = cls(
            month_year=month_year,
            global_rank_change_members=global_rank_change_members,
            global_rank_pct_change_members=global_rank_pct_change_members,
        )

        subreddit_rank_change_row.additional_properties = d
        return subreddit_rank_change_row

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
