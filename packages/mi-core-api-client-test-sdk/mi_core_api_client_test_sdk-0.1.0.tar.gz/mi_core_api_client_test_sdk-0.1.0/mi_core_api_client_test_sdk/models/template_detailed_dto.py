import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_import_data_schema import ProjectImportDataSchema


T = TypeVar("T", bound="TemplateDetailedDTO")


@_attrs_define
class TemplateDetailedDTO:
    """
    Attributes:
        name (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        data (ProjectImportDataSchema):
        id (Union[Unset, UUID]):
    """

    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    data: "ProjectImportDataSchema"
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        data = self.data.to_dict()

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "data": data,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_import_data_schema import ProjectImportDataSchema

        d = dict(src_dict)
        name = d.pop("name")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        data = ProjectImportDataSchema.from_dict(d.pop("data"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        template_detailed_dto = cls(
            name=name,
            created_at=created_at,
            updated_at=updated_at,
            data=data,
            id=id,
        )

        template_detailed_dto.additional_properties = d
        return template_detailed_dto

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
