from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="YTMetricsChangeRow")


@_attrs_define
class YTMetricsChangeRow:
    """
    Attributes:
        month_year (str):
        channel_primary_topic (str):
        channel_country (str):
        total_views (int):
        subscribers (int):
        topic_rank_by_views (int):
        topic_rank_by_subs (int):
        country_rank_by_views (int):
        country_rank_by_subs (int):
        global_rank_by_views (int):
        global_rank_by_subs (int):
    """

    month_year: str
    channel_primary_topic: str
    channel_country: str
    total_views: int
    subscribers: int
    topic_rank_by_views: int
    topic_rank_by_subs: int
    country_rank_by_views: int
    country_rank_by_subs: int
    global_rank_by_views: int
    global_rank_by_subs: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        month_year = self.month_year

        channel_primary_topic = self.channel_primary_topic

        channel_country = self.channel_country

        total_views = self.total_views

        subscribers = self.subscribers

        topic_rank_by_views = self.topic_rank_by_views

        topic_rank_by_subs = self.topic_rank_by_subs

        country_rank_by_views = self.country_rank_by_views

        country_rank_by_subs = self.country_rank_by_subs

        global_rank_by_views = self.global_rank_by_views

        global_rank_by_subs = self.global_rank_by_subs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "monthYear": month_year,
                "channelPrimaryTopic": channel_primary_topic,
                "channelCountry": channel_country,
                "totalViews": total_views,
                "subscribers": subscribers,
                "topicRankByViews": topic_rank_by_views,
                "topicRankBySubs": topic_rank_by_subs,
                "countryRankByViews": country_rank_by_views,
                "countryRankBySubs": country_rank_by_subs,
                "globalRankByViews": global_rank_by_views,
                "globalRankBySubs": global_rank_by_subs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        month_year = d.pop("monthYear")

        channel_primary_topic = d.pop("channelPrimaryTopic")

        channel_country = d.pop("channelCountry")

        total_views = d.pop("totalViews")

        subscribers = d.pop("subscribers")

        topic_rank_by_views = d.pop("topicRankByViews")

        topic_rank_by_subs = d.pop("topicRankBySubs")

        country_rank_by_views = d.pop("countryRankByViews")

        country_rank_by_subs = d.pop("countryRankBySubs")

        global_rank_by_views = d.pop("globalRankByViews")

        global_rank_by_subs = d.pop("globalRankBySubs")

        yt_metrics_change_row = cls(
            month_year=month_year,
            channel_primary_topic=channel_primary_topic,
            channel_country=channel_country,
            total_views=total_views,
            subscribers=subscribers,
            topic_rank_by_views=topic_rank_by_views,
            topic_rank_by_subs=topic_rank_by_subs,
            country_rank_by_views=country_rank_by_views,
            country_rank_by_subs=country_rank_by_subs,
            global_rank_by_views=global_rank_by_views,
            global_rank_by_subs=global_rank_by_subs,
        )

        yt_metrics_change_row.additional_properties = d
        return yt_metrics_change_row

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
