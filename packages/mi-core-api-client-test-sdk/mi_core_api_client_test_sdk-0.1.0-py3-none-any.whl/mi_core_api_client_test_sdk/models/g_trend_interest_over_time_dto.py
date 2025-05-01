import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.interval_type import IntervalType
from ..types import UNSET, Unset

T = TypeVar("T", bound="GTrendInterestOverTimeDTO")


@_attrs_define
class GTrendInterestOverTimeDTO:
    """
    Attributes:
        topic_id (UUID):
        start_date (datetime.datetime):
        end_date (datetime.datetime):
        value (int):
        interval (Union[Unset, IntervalType]): Enumeration class representing interval types.
    """

    topic_id: UUID
    start_date: datetime.datetime
    end_date: datetime.datetime
    value: int
    interval: Union[Unset, IntervalType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        topic_id = str(self.topic_id)

        start_date = self.start_date.isoformat()

        end_date = self.end_date.isoformat()

        value = self.value

        interval: Union[Unset, str] = UNSET
        if not isinstance(self.interval, Unset):
            interval = self.interval.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topicId": topic_id,
                "startDate": start_date,
                "endDate": end_date,
                "value": value,
            }
        )
        if interval is not UNSET:
            field_dict["interval"] = interval

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        topic_id = UUID(d.pop("topicId"))

        start_date = isoparse(d.pop("startDate"))

        end_date = isoparse(d.pop("endDate"))

        value = d.pop("value")

        _interval = d.pop("interval", UNSET)
        interval: Union[Unset, IntervalType]
        if isinstance(_interval, Unset):
            interval = UNSET
        else:
            interval = IntervalType(_interval)

        g_trend_interest_over_time_dto = cls(
            topic_id=topic_id,
            start_date=start_date,
            end_date=end_date,
            value=value,
            interval=interval,
        )

        g_trend_interest_over_time_dto.additional_properties = d
        return g_trend_interest_over_time_dto

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
