from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectSourcesCollectionStats")


@_attrs_define
class ProjectSourcesCollectionStats:
    """
    Attributes:
        total_count (Union[Unset, int]):  Default: 0.
        success_count (Union[Unset, int]):  Default: 0.
        failed_count (Union[Unset, int]):  Default: 0.
    """

    total_count: Union[Unset, int] = 0
    success_count: Union[Unset, int] = 0
    failed_count: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_count = self.total_count

        success_count = self.success_count

        failed_count = self.failed_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_count is not UNSET:
            field_dict["total_count"] = total_count
        if success_count is not UNSET:
            field_dict["success_count"] = success_count
        if failed_count is not UNSET:
            field_dict["failed_count"] = failed_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_count = d.pop("total_count", UNSET)

        success_count = d.pop("success_count", UNSET)

        failed_count = d.pop("failed_count", UNSET)

        project_sources_collection_stats = cls(
            total_count=total_count,
            success_count=success_count,
            failed_count=failed_count,
        )

        project_sources_collection_stats.additional_properties = d
        return project_sources_collection_stats

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
