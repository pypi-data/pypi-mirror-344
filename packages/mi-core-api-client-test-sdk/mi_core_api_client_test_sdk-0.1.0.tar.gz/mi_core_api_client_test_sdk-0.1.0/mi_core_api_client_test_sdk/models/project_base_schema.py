from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_column_dto import CustomColumnDTO


T = TypeVar("T", bound="ProjectBaseSchema")


@_attrs_define
class ProjectBaseSchema:
    """
    Attributes:
        name (str):
        description (str):
        id (Union[Unset, UUID]):
        custom_fields (Union[Unset, list['CustomColumnDTO']]):
    """

    name: str
    description: str
    id: Union[Unset, UUID] = UNSET
    custom_fields: Union[Unset, list["CustomColumnDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        custom_fields: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = []
            for custom_fields_item_data in self.custom_fields:
                custom_fields_item = custom_fields_item_data.to_dict()
                custom_fields.append(custom_fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_column_dto import CustomColumnDTO

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        custom_fields = []
        _custom_fields = d.pop("customFields", UNSET)
        for custom_fields_item_data in _custom_fields or []:
            custom_fields_item = CustomColumnDTO.from_dict(custom_fields_item_data)

            custom_fields.append(custom_fields_item)

        project_base_schema = cls(
            name=name,
            description=description,
            id=id,
            custom_fields=custom_fields,
        )

        project_base_schema.additional_properties = d
        return project_base_schema

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
