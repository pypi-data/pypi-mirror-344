from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trend_chart_description import TrendChartDescription

T = TypeVar("T", bound="GTrendCalculatedInterestMetrics")


@_attrs_define
class GTrendCalculatedInterestMetrics:
    """
    Attributes:
        growth_90_d_value (int):
        growth_90_d_vs_prev_period (int):
        growth_5_y_value (int):
        growth_5_y_year_over_year (int):
        annual_average_value (int):
        annual_description (TrendChartDescription): Enumeration class representing trend chart descriptions.
    """

    growth_90_d_value: int
    growth_90_d_vs_prev_period: int
    growth_5_y_value: int
    growth_5_y_year_over_year: int
    annual_average_value: int
    annual_description: TrendChartDescription
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        growth_90_d_value = self.growth_90_d_value

        growth_90_d_vs_prev_period = self.growth_90_d_vs_prev_period

        growth_5_y_value = self.growth_5_y_value

        growth_5_y_year_over_year = self.growth_5_y_year_over_year

        annual_average_value = self.annual_average_value

        annual_description = self.annual_description.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "growth90dValue": growth_90_d_value,
                "growth90dVsPrevPeriod": growth_90_d_vs_prev_period,
                "growth5yValue": growth_5_y_value,
                "growth5yYearOverYear": growth_5_y_year_over_year,
                "annualAverageValue": annual_average_value,
                "annualDescription": annual_description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        growth_90_d_value = d.pop("growth90dValue")

        growth_90_d_vs_prev_period = d.pop("growth90dVsPrevPeriod")

        growth_5_y_value = d.pop("growth5yValue")

        growth_5_y_year_over_year = d.pop("growth5yYearOverYear")

        annual_average_value = d.pop("annualAverageValue")

        annual_description = TrendChartDescription(d.pop("annualDescription"))

        g_trend_calculated_interest_metrics = cls(
            growth_90_d_value=growth_90_d_value,
            growth_90_d_vs_prev_period=growth_90_d_vs_prev_period,
            growth_5_y_value=growth_5_y_value,
            growth_5_y_year_over_year=growth_5_y_year_over_year,
            annual_average_value=annual_average_value,
            annual_description=annual_description,
        )

        g_trend_calculated_interest_metrics.additional_properties = d
        return g_trend_calculated_interest_metrics

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
