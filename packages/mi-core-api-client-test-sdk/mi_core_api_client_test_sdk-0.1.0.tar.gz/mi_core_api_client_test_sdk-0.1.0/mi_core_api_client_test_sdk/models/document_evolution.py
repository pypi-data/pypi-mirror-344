from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.observation import Observation


T = TypeVar("T", bound="DocumentEvolution")


@_attrs_define
class DocumentEvolution:
    """
    Attributes:
        document_id (UUID):
        title (str):
        description (str):
        metric_records (list['Observation']):
    """

    document_id: UUID
    title: str
    description: str
    metric_records: list["Observation"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        document_id = str(self.document_id)

        title = self.title

        description = self.description

        metric_records = []
        for metric_records_item_data in self.metric_records:
            metric_records_item = metric_records_item_data.to_dict()
            metric_records.append(metric_records_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documentId": document_id,
                "title": title,
                "description": description,
                "metricRecords": metric_records,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.observation import Observation

        d = dict(src_dict)
        document_id = UUID(d.pop("documentId"))

        title = d.pop("title")

        description = d.pop("description")

        metric_records = []
        _metric_records = d.pop("metricRecords")
        for metric_records_item_data in _metric_records:
            metric_records_item = Observation.from_dict(metric_records_item_data)

            metric_records.append(metric_records_item)

        document_evolution = cls(
            document_id=document_id,
            title=title,
            description=description,
            metric_records=metric_records,
        )

        document_evolution.additional_properties = d
        return document_evolution

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
