from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.yt_daily_row import YTDailyRow
    from ..models.yt_metrics_change_row import YTMetricsChangeRow
    from ..models.yt_rank_change_row import YTRankChangeRow


T = TypeVar("T", bound="YTResponseRow")


@_attrs_define
class YTResponseRow:
    """
    Attributes:
        document_id (str):
        channel_primary_topic (str):
        channel_country (str):
        daily_metrics (list['YTDailyRow']):
        monthly_ranks (list['YTRankChangeRow']):
        monthly_metrics (list['YTMetricsChangeRow']):
    """

    document_id: str
    channel_primary_topic: str
    channel_country: str
    daily_metrics: list["YTDailyRow"]
    monthly_ranks: list["YTRankChangeRow"]
    monthly_metrics: list["YTMetricsChangeRow"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        document_id = self.document_id

        channel_primary_topic = self.channel_primary_topic

        channel_country = self.channel_country

        daily_metrics = []
        for daily_metrics_item_data in self.daily_metrics:
            daily_metrics_item = daily_metrics_item_data.to_dict()
            daily_metrics.append(daily_metrics_item)

        monthly_ranks = []
        for monthly_ranks_item_data in self.monthly_ranks:
            monthly_ranks_item = monthly_ranks_item_data.to_dict()
            monthly_ranks.append(monthly_ranks_item)

        monthly_metrics = []
        for monthly_metrics_item_data in self.monthly_metrics:
            monthly_metrics_item = monthly_metrics_item_data.to_dict()
            monthly_metrics.append(monthly_metrics_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documentId": document_id,
                "channelPrimaryTopic": channel_primary_topic,
                "channelCountry": channel_country,
                "dailyMetrics": daily_metrics,
                "monthlyRanks": monthly_ranks,
                "monthlyMetrics": monthly_metrics,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.yt_daily_row import YTDailyRow
        from ..models.yt_metrics_change_row import YTMetricsChangeRow
        from ..models.yt_rank_change_row import YTRankChangeRow

        d = dict(src_dict)
        document_id = d.pop("documentId")

        channel_primary_topic = d.pop("channelPrimaryTopic")

        channel_country = d.pop("channelCountry")

        daily_metrics = []
        _daily_metrics = d.pop("dailyMetrics")
        for daily_metrics_item_data in _daily_metrics:
            daily_metrics_item = YTDailyRow.from_dict(daily_metrics_item_data)

            daily_metrics.append(daily_metrics_item)

        monthly_ranks = []
        _monthly_ranks = d.pop("monthlyRanks")
        for monthly_ranks_item_data in _monthly_ranks:
            monthly_ranks_item = YTRankChangeRow.from_dict(monthly_ranks_item_data)

            monthly_ranks.append(monthly_ranks_item)

        monthly_metrics = []
        _monthly_metrics = d.pop("monthlyMetrics")
        for monthly_metrics_item_data in _monthly_metrics:
            monthly_metrics_item = YTMetricsChangeRow.from_dict(monthly_metrics_item_data)

            monthly_metrics.append(monthly_metrics_item)

        yt_response_row = cls(
            document_id=document_id,
            channel_primary_topic=channel_primary_topic,
            channel_country=channel_country,
            daily_metrics=daily_metrics,
            monthly_ranks=monthly_ranks,
            monthly_metrics=monthly_metrics,
        )

        yt_response_row.additional_properties = d
        return yt_response_row

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
