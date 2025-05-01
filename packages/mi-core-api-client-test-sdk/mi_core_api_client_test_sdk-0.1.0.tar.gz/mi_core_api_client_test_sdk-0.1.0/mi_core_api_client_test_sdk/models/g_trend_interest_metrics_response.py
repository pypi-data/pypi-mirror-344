from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.g_trend_calculated_interest_metrics import GTrendCalculatedInterestMetrics
    from ..models.g_trend_interest_over_time_dto import GTrendInterestOverTimeDTO


T = TypeVar("T", bound="GTrendInterestMetricsResponse")


@_attrs_define
class GTrendInterestMetricsResponse:
    """
    Attributes:
        last_6_months_trends (list['GTrendInterestOverTimeDTO']):
        metrics (GTrendCalculatedInterestMetrics):
        overview (str):
    """

    last_6_months_trends: list["GTrendInterestOverTimeDTO"]
    metrics: "GTrendCalculatedInterestMetrics"
    overview: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        last_6_months_trends = []
        for last_6_months_trends_item_data in self.last_6_months_trends:
            last_6_months_trends_item = last_6_months_trends_item_data.to_dict()
            last_6_months_trends.append(last_6_months_trends_item)

        metrics = self.metrics.to_dict()

        overview = self.overview

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "last6MonthsTrends": last_6_months_trends,
                "metrics": metrics,
                "overview": overview,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.g_trend_calculated_interest_metrics import GTrendCalculatedInterestMetrics
        from ..models.g_trend_interest_over_time_dto import GTrendInterestOverTimeDTO

        d = dict(src_dict)
        last_6_months_trends = []
        _last_6_months_trends = d.pop("last6MonthsTrends")
        for last_6_months_trends_item_data in _last_6_months_trends:
            last_6_months_trends_item = GTrendInterestOverTimeDTO.from_dict(last_6_months_trends_item_data)

            last_6_months_trends.append(last_6_months_trends_item)

        metrics = GTrendCalculatedInterestMetrics.from_dict(d.pop("metrics"))

        overview = d.pop("overview")

        g_trend_interest_metrics_response = cls(
            last_6_months_trends=last_6_months_trends,
            metrics=metrics,
            overview=overview,
        )

        g_trend_interest_metrics_response.additional_properties = d
        return g_trend_interest_metrics_response

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
