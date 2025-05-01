from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SourceStatusResponse")


@_attrs_define
class SourceStatusResponse:
    """
    Attributes:
        metadata_status (JobStatus): Enumeration class representing job statuses.

            Attributes:
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
        data_status (JobStatus): Enumeration class representing job statuses.

            Attributes:
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
        id (Union[Unset, UUID]):
    """

    metadata_status: JobStatus
    data_status: JobStatus
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_status = self.metadata_status.value

        data_status = self.data_status.value

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadataStatus": metadata_status,
                "dataStatus": data_status,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        metadata_status = JobStatus(d.pop("metadataStatus"))

        data_status = JobStatus(d.pop("dataStatus"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        source_status_response = cls(
            metadata_status=metadata_status,
            data_status=data_status,
            id=id,
        )

        source_status_response.additional_properties = d
        return source_status_response

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
