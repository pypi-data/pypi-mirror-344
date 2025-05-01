from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_lookup_model import DataLookupModel

T = TypeVar("T", bound="AvailableDataPoints")


@_attrs_define
class AvailableDataPoints:
    """
    Attributes:
        join_model (DataLookupModel): Enumeration class representing data lookup models.
        fields (list[str]):
    """

    join_model: DataLookupModel
    fields: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        join_model = self.join_model.value

        fields = self.fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "joinModel": join_model,
                "fields": fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        join_model = DataLookupModel(d.pop("joinModel"))

        fields = cast(list[str], d.pop("fields"))

        available_data_points = cls(
            join_model=join_model,
            fields=fields,
        )

        available_data_points.additional_properties = d
        return available_data_points

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
