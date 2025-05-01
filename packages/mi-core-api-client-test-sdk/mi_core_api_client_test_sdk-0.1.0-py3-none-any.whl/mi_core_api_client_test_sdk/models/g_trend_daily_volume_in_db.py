import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GTrendDailyVolumeInDB")


@_attrs_define
class GTrendDailyVolumeInDB:
    """
    Attributes:
        date (datetime.date):
        query_text (str):
        volume (int):
        serpapi_response_id (UUID):
        id (UUID):
        topic_id (Union[None, UUID, Unset]):
    """

    date: datetime.date
    query_text: str
    volume: int
    serpapi_response_id: UUID
    id: UUID
    topic_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        query_text = self.query_text

        volume = self.volume

        serpapi_response_id = str(self.serpapi_response_id)

        id = str(self.id)

        topic_id: Union[None, Unset, str]
        if isinstance(self.topic_id, Unset):
            topic_id = UNSET
        elif isinstance(self.topic_id, UUID):
            topic_id = str(self.topic_id)
        else:
            topic_id = self.topic_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "queryText": query_text,
                "volume": volume,
                "serpapiResponseId": serpapi_response_id,
                "id": id,
            }
        )
        if topic_id is not UNSET:
            field_dict["topicId"] = topic_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = isoparse(d.pop("date")).date()

        query_text = d.pop("queryText")

        volume = d.pop("volume")

        serpapi_response_id = UUID(d.pop("serpapiResponseId"))

        id = UUID(d.pop("id"))

        def _parse_topic_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                topic_id_type_0 = UUID(data)

                return topic_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        topic_id = _parse_topic_id(d.pop("topicId", UNSET))

        g_trend_daily_volume_in_db = cls(
            date=date,
            query_text=query_text,
            volume=volume,
            serpapi_response_id=serpapi_response_id,
            id=id,
            topic_id=topic_id,
        )

        g_trend_daily_volume_in_db.additional_properties = d
        return g_trend_daily_volume_in_db

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
