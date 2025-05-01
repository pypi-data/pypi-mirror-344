from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChannelSummaryWithArchetypes")


@_attrs_define
class ChannelSummaryWithArchetypes:
    """
    Attributes:
        channel_summary_id (UUID):
        archetypes (Union[None, Unset, list[UUID]]):
    """

    channel_summary_id: UUID
    archetypes: Union[None, Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel_summary_id = str(self.channel_summary_id)

        archetypes: Union[None, Unset, list[str]]
        if isinstance(self.archetypes, Unset):
            archetypes = UNSET
        elif isinstance(self.archetypes, list):
            archetypes = []
            for archetypes_type_0_item_data in self.archetypes:
                archetypes_type_0_item = str(archetypes_type_0_item_data)
                archetypes.append(archetypes_type_0_item)

        else:
            archetypes = self.archetypes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_summary_id": channel_summary_id,
            }
        )
        if archetypes is not UNSET:
            field_dict["archetypes"] = archetypes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel_summary_id = UUID(d.pop("channel_summary_id"))

        def _parse_archetypes(data: object) -> Union[None, Unset, list[UUID]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                archetypes_type_0 = []
                _archetypes_type_0 = data
                for archetypes_type_0_item_data in _archetypes_type_0:
                    archetypes_type_0_item = UUID(archetypes_type_0_item_data)

                    archetypes_type_0.append(archetypes_type_0_item)

                return archetypes_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[UUID]], data)

        archetypes = _parse_archetypes(d.pop("archetypes", UNSET))

        channel_summary_with_archetypes = cls(
            channel_summary_id=channel_summary_id,
            archetypes=archetypes,
        )

        channel_summary_with_archetypes.additional_properties = d
        return channel_summary_with_archetypes

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
