from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_column_type import CustomColumnType
from ..models.custom_field_type import CustomFieldType
from ..models.data_lookup_model import DataLookupModel

T = TypeVar("T", bound="CreateCustomColumnDataLookup")


@_attrs_define
class CreateCustomColumnDataLookup:
    """
    Attributes:
        lookup_model (DataLookupModel): Enumeration class representing data lookup models.
        lookup_field (str):
        type_ (CustomColumnType): Enumeration class representing custom column types.
        name (str):
        content_type (CustomFieldType): Enumeration class representing custom field types.
        project_id (UUID):
    """

    lookup_model: DataLookupModel
    lookup_field: str
    type_: CustomColumnType
    name: str
    content_type: CustomFieldType
    project_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lookup_model = self.lookup_model.value

        lookup_field = self.lookup_field

        type_ = self.type_.value

        name = self.name

        content_type = self.content_type.value

        project_id = str(self.project_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lookup_model": lookup_model,
                "lookup_field": lookup_field,
                "type": type_,
                "name": name,
                "content_type": content_type,
                "project_id": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lookup_model = DataLookupModel(d.pop("lookup_model"))

        lookup_field = d.pop("lookup_field")

        type_ = CustomColumnType(d.pop("type"))

        name = d.pop("name")

        content_type = CustomFieldType(d.pop("content_type"))

        project_id = UUID(d.pop("project_id"))

        create_custom_column_data_lookup = cls(
            lookup_model=lookup_model,
            lookup_field=lookup_field,
            type_=type_,
            name=name,
            content_type=content_type,
            project_id=project_id,
        )

        create_custom_column_data_lookup.additional_properties = d
        return create_custom_column_data_lookup

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
