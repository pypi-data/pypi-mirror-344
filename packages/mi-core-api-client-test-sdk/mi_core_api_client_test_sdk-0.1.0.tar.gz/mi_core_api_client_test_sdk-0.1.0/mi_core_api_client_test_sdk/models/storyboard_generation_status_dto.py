from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.storyboard_generation_status_enum import StoryboardGenerationStatusEnum

T = TypeVar("T", bound="StoryboardGenerationStatusDTO")


@_attrs_define
class StoryboardGenerationStatusDTO:
    """
    Attributes:
        storyboard_id (UUID):
        status (StoryboardGenerationStatusEnum): Enumeration class representing storyboard generation status.
    """

    storyboard_id: UUID
    status: StoryboardGenerationStatusEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        storyboard_id = str(self.storyboard_id)

        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "storyboardId": storyboard_id,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        storyboard_id = UUID(d.pop("storyboardId"))

        status = StoryboardGenerationStatusEnum(d.pop("status"))

        storyboard_generation_status_dto = cls(
            storyboard_id=storyboard_id,
            status=status,
        )

        storyboard_generation_status_dto.additional_properties = d
        return storyboard_generation_status_dto

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
