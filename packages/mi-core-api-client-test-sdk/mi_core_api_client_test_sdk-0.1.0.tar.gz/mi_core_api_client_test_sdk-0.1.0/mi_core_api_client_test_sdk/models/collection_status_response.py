from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CollectionStatusResponse")


@_attrs_define
class CollectionStatusResponse:
    """
    Attributes:
        collection_status (JobStatus): Enumeration class representing job statuses.

            Attributes:
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
        total_number (int):
        collected_number (int):
        created (Union[Unset, int]):  Default: 0.
        processing (Union[Unset, int]):  Default: 0.
        completed (Union[Unset, int]):  Default: 0.
        failed (Union[Unset, int]):  Default: 0.
    """

    collection_status: JobStatus
    total_number: int
    collected_number: int
    created: Union[Unset, int] = 0
    processing: Union[Unset, int] = 0
    completed: Union[Unset, int] = 0
    failed: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        collection_status = self.collection_status.value

        total_number = self.total_number

        collected_number = self.collected_number

        created = self.created

        processing = self.processing

        completed = self.completed

        failed = self.failed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "collectionStatus": collection_status,
                "totalNumber": total_number,
                "collectedNumber": collected_number,
            }
        )
        if created is not UNSET:
            field_dict["created"] = created
        if processing is not UNSET:
            field_dict["processing"] = processing
        if completed is not UNSET:
            field_dict["completed"] = completed
        if failed is not UNSET:
            field_dict["failed"] = failed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        collection_status = JobStatus(d.pop("collectionStatus"))

        total_number = d.pop("totalNumber")

        collected_number = d.pop("collectedNumber")

        created = d.pop("created", UNSET)

        processing = d.pop("processing", UNSET)

        completed = d.pop("completed", UNSET)

        failed = d.pop("failed", UNSET)

        collection_status_response = cls(
            collection_status=collection_status,
            total_number=total_number,
            collected_number=collected_number,
            created=created,
            processing=processing,
            completed=completed,
            failed=failed,
        )

        collection_status_response.additional_properties = d
        return collection_status_response

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
