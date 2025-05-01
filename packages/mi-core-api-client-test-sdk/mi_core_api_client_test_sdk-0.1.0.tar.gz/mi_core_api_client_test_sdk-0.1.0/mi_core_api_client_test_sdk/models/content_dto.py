import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ContentDTO")


@_attrs_define
class ContentDTO:
    """
    Attributes:
        value (Union[float, int]):
        timestamp (datetime.datetime):
        document_id (UUID):
    """

    value: Union[float, int]
    timestamp: datetime.datetime
    document_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value: Union[float, int]
        value = self.value

        timestamp = self.timestamp.isoformat()

        document_id = str(self.document_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "timestamp": timestamp,
                "documentId": document_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_value(data: object) -> Union[float, int]:
            return cast(Union[float, int], data)

        value = _parse_value(d.pop("value"))

        timestamp = isoparse(d.pop("timestamp"))

        document_id = UUID(d.pop("documentId"))

        content_dto = cls(
            value=value,
            timestamp=timestamp,
            document_id=document_id,
        )

        content_dto.additional_properties = d
        return content_dto

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
