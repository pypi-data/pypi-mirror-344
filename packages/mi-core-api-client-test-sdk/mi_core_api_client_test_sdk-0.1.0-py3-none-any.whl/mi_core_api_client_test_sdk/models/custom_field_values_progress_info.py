from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldValuesProgressInfo")


@_attrs_define
class CustomFieldValuesProgressInfo:
    """
    Attributes:
        custom_field_id (UUID):
        total (Union[Unset, int]):  Default: 0.
        in_progress (Union[Unset, int]):  Default: 0.
        completed (Union[Unset, int]):  Default: 0.
        failed (Union[Unset, int]):  Default: 0.
    """

    custom_field_id: UUID
    total: Union[Unset, int] = 0
    in_progress: Union[Unset, int] = 0
    completed: Union[Unset, int] = 0
    failed: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        custom_field_id = str(self.custom_field_id)

        total = self.total

        in_progress = self.in_progress

        completed = self.completed

        failed = self.failed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customFieldId": custom_field_id,
            }
        )
        if total is not UNSET:
            field_dict["total"] = total
        if in_progress is not UNSET:
            field_dict["inProgress"] = in_progress
        if completed is not UNSET:
            field_dict["completed"] = completed
        if failed is not UNSET:
            field_dict["failed"] = failed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        custom_field_id = UUID(d.pop("customFieldId"))

        total = d.pop("total", UNSET)

        in_progress = d.pop("inProgress", UNSET)

        completed = d.pop("completed", UNSET)

        failed = d.pop("failed", UNSET)

        custom_field_values_progress_info = cls(
            custom_field_id=custom_field_id,
            total=total,
            in_progress=in_progress,
            completed=completed,
            failed=failed,
        )

        custom_field_values_progress_info.additional_properties = d
        return custom_field_values_progress_info

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
