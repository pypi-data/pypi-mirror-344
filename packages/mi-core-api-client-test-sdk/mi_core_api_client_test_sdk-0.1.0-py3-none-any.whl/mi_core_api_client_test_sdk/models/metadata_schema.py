from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metadata_status import MetadataStatus

T = TypeVar("T", bound="MetadataSchema")


@_attrs_define
class MetadataSchema:
    """
    Attributes:
        total_result_count (int):
        complete_results_count (int):
        error_results_count (int):
        time_taken (str):
        created_at (str):
        processed_at (str):
        status (MetadataStatus):
    """

    total_result_count: int
    complete_results_count: int
    error_results_count: int
    time_taken: str
    created_at: str
    processed_at: str
    status: MetadataStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_result_count = self.total_result_count

        complete_results_count = self.complete_results_count

        error_results_count = self.error_results_count

        time_taken = self.time_taken

        created_at = self.created_at

        processed_at = self.processed_at

        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "totalResultCount": total_result_count,
                "completeResultsCount": complete_results_count,
                "errorResultsCount": error_results_count,
                "timeTaken": time_taken,
                "createdAt": created_at,
                "processedAt": processed_at,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_result_count = d.pop("totalResultCount")

        complete_results_count = d.pop("completeResultsCount")

        error_results_count = d.pop("errorResultsCount")

        time_taken = d.pop("timeTaken")

        created_at = d.pop("createdAt")

        processed_at = d.pop("processedAt")

        status = MetadataStatus(d.pop("status"))

        metadata_schema = cls(
            total_result_count=total_result_count,
            complete_results_count=complete_results_count,
            error_results_count=error_results_count,
            time_taken=time_taken,
            created_at=created_at,
            processed_at=processed_at,
            status=status,
        )

        metadata_schema.additional_properties = d
        return metadata_schema

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
