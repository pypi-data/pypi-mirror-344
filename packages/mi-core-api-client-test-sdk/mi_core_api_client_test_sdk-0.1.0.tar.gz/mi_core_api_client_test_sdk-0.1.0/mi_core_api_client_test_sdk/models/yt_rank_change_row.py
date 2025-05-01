from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="YTRankChangeRow")


@_attrs_define
class YTRankChangeRow:
    """
    Attributes:
        month_year (str):
        global_rank_change_views (Union[None, int]):
        global_rank_change_subs (Union[None, int]):
        global_rank_pct_change_views (Union[None, float]):
        global_rank_pct_change_subs (Union[None, float]):
        country_rank_change_views (Union[None, int]):
        country_rank_change_subs (Union[None, int]):
        country_rank_pct_change_views (Union[None, float]):
        country_rank_pct_change_subs (Union[None, float]):
        topic_rank_change_views (Union[None, int]):
        topic_rank_change_subs (Union[None, int]):
        topic_rank_pct_change_views (Union[None, float]):
        topic_rank_pct_change_subs (Union[None, float]):
    """

    month_year: str
    global_rank_change_views: Union[None, int]
    global_rank_change_subs: Union[None, int]
    global_rank_pct_change_views: Union[None, float]
    global_rank_pct_change_subs: Union[None, float]
    country_rank_change_views: Union[None, int]
    country_rank_change_subs: Union[None, int]
    country_rank_pct_change_views: Union[None, float]
    country_rank_pct_change_subs: Union[None, float]
    topic_rank_change_views: Union[None, int]
    topic_rank_change_subs: Union[None, int]
    topic_rank_pct_change_views: Union[None, float]
    topic_rank_pct_change_subs: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month_year = self.month_year

        global_rank_change_views: Union[None, int]
        global_rank_change_views = self.global_rank_change_views

        global_rank_change_subs: Union[None, int]
        global_rank_change_subs = self.global_rank_change_subs

        global_rank_pct_change_views: Union[None, float]
        global_rank_pct_change_views = self.global_rank_pct_change_views

        global_rank_pct_change_subs: Union[None, float]
        global_rank_pct_change_subs = self.global_rank_pct_change_subs

        country_rank_change_views: Union[None, int]
        country_rank_change_views = self.country_rank_change_views

        country_rank_change_subs: Union[None, int]
        country_rank_change_subs = self.country_rank_change_subs

        country_rank_pct_change_views: Union[None, float]
        country_rank_pct_change_views = self.country_rank_pct_change_views

        country_rank_pct_change_subs: Union[None, float]
        country_rank_pct_change_subs = self.country_rank_pct_change_subs

        topic_rank_change_views: Union[None, int]
        topic_rank_change_views = self.topic_rank_change_views

        topic_rank_change_subs: Union[None, int]
        topic_rank_change_subs = self.topic_rank_change_subs

        topic_rank_pct_change_views: Union[None, float]
        topic_rank_pct_change_views = self.topic_rank_pct_change_views

        topic_rank_pct_change_subs: Union[None, float]
        topic_rank_pct_change_subs = self.topic_rank_pct_change_subs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "monthYear": month_year,
                "globalRankChangeViews": global_rank_change_views,
                "globalRankChangeSubs": global_rank_change_subs,
                "globalRankPctChangeViews": global_rank_pct_change_views,
                "globalRankPctChangeSubs": global_rank_pct_change_subs,
                "countryRankChangeViews": country_rank_change_views,
                "countryRankChangeSubs": country_rank_change_subs,
                "countryRankPctChangeViews": country_rank_pct_change_views,
                "countryRankPctChangeSubs": country_rank_pct_change_subs,
                "topicRankChangeViews": topic_rank_change_views,
                "topicRankChangeSubs": topic_rank_change_subs,
                "topicRankPctChangeViews": topic_rank_pct_change_views,
                "topicRankPctChangeSubs": topic_rank_pct_change_subs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month_year = d.pop("monthYear")

        def _parse_global_rank_change_views(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        global_rank_change_views = _parse_global_rank_change_views(d.pop("globalRankChangeViews"))

        def _parse_global_rank_change_subs(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        global_rank_change_subs = _parse_global_rank_change_subs(d.pop("globalRankChangeSubs"))

        def _parse_global_rank_pct_change_views(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        global_rank_pct_change_views = _parse_global_rank_pct_change_views(d.pop("globalRankPctChangeViews"))

        def _parse_global_rank_pct_change_subs(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        global_rank_pct_change_subs = _parse_global_rank_pct_change_subs(d.pop("globalRankPctChangeSubs"))

        def _parse_country_rank_change_views(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        country_rank_change_views = _parse_country_rank_change_views(d.pop("countryRankChangeViews"))

        def _parse_country_rank_change_subs(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        country_rank_change_subs = _parse_country_rank_change_subs(d.pop("countryRankChangeSubs"))

        def _parse_country_rank_pct_change_views(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        country_rank_pct_change_views = _parse_country_rank_pct_change_views(d.pop("countryRankPctChangeViews"))

        def _parse_country_rank_pct_change_subs(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        country_rank_pct_change_subs = _parse_country_rank_pct_change_subs(d.pop("countryRankPctChangeSubs"))

        def _parse_topic_rank_change_views(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        topic_rank_change_views = _parse_topic_rank_change_views(d.pop("topicRankChangeViews"))

        def _parse_topic_rank_change_subs(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        topic_rank_change_subs = _parse_topic_rank_change_subs(d.pop("topicRankChangeSubs"))

        def _parse_topic_rank_pct_change_views(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        topic_rank_pct_change_views = _parse_topic_rank_pct_change_views(d.pop("topicRankPctChangeViews"))

        def _parse_topic_rank_pct_change_subs(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        topic_rank_pct_change_subs = _parse_topic_rank_pct_change_subs(d.pop("topicRankPctChangeSubs"))

        yt_rank_change_row = cls(
            month_year=month_year,
            global_rank_change_views=global_rank_change_views,
            global_rank_change_subs=global_rank_change_subs,
            global_rank_pct_change_views=global_rank_pct_change_views,
            global_rank_pct_change_subs=global_rank_pct_change_subs,
            country_rank_change_views=country_rank_change_views,
            country_rank_change_subs=country_rank_change_subs,
            country_rank_pct_change_views=country_rank_pct_change_views,
            country_rank_pct_change_subs=country_rank_pct_change_subs,
            topic_rank_change_views=topic_rank_change_views,
            topic_rank_change_subs=topic_rank_change_subs,
            topic_rank_pct_change_views=topic_rank_pct_change_views,
            topic_rank_pct_change_subs=topic_rank_pct_change_subs,
        )

        yt_rank_change_row.additional_properties = d
        return yt_rank_change_row

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
