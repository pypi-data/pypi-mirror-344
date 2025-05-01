from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_field_type import CustomFieldType
from ..models.data_lookup_model import DataLookupModel

T = TypeVar("T", bound="AutoGenerateColumnNameDataLookup")


@_attrs_define
class AutoGenerateColumnNameDataLookup:
    """
    Attributes:
        lookup_model (DataLookupModel): Enumeration class representing data lookup models.
        lookup_field (str):
        type_ (Literal['data_lookup']):
        content_type (CustomFieldType): Enumeration class representing custom field types.
    """

    lookup_model: DataLookupModel
    lookup_field: str
    type_: Literal["data_lookup"]
    content_type: CustomFieldType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lookup_model = self.lookup_model.value

        lookup_field = self.lookup_field

        type_ = self.type_

        content_type = self.content_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lookup_model": lookup_model,
                "lookup_field": lookup_field,
                "type": type_,
                "content_type": content_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lookup_model = DataLookupModel(d.pop("lookup_model"))

        lookup_field = d.pop("lookup_field")

        type_ = cast(Literal["data_lookup"], d.pop("type"))
        if type_ != "data_lookup":
            raise ValueError(f"type must match const 'data_lookup', got '{type_}'")

        content_type = CustomFieldType(d.pop("content_type"))

        auto_generate_column_name_data_lookup = cls(
            lookup_model=lookup_model,
            lookup_field=lookup_field,
            type_=type_,
            content_type=content_type,
        )

        auto_generate_column_name_data_lookup.additional_properties = d
        return auto_generate_column_name_data_lookup

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
