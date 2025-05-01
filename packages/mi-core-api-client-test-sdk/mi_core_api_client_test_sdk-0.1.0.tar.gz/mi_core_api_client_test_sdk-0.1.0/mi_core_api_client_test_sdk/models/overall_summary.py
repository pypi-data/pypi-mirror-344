import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="OverallSummary")


@_attrs_define
class OverallSummary:
    """
    Attributes:
        documents_count (int):
        last_updated (datetime.datetime):
        entities_count (int):
    """

    documents_count: int
    last_updated: datetime.datetime
    entities_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        documents_count = self.documents_count

        last_updated = self.last_updated.isoformat()

        entities_count = self.entities_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documentsCount": documents_count,
                "lastUpdated": last_updated,
                "entitiesCount": entities_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        documents_count = d.pop("documentsCount")

        last_updated = isoparse(d.pop("lastUpdated"))

        entities_count = d.pop("entitiesCount")

        overall_summary = cls(
            documents_count=documents_count,
            last_updated=last_updated,
            entities_count=entities_count,
        )

        overall_summary.additional_properties = d
        return overall_summary

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
