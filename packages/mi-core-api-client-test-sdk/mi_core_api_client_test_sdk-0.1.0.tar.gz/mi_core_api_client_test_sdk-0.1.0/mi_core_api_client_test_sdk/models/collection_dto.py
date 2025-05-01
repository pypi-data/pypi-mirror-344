import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CollectionDTO")


@_attrs_define
class CollectionDTO:
    """
    Attributes:
        name (str):
        updated_at (datetime.date):
        id (Union[Unset, UUID]):
        source_count (Union[Unset, int]):  Default: 0.
    """

    name: str
    updated_at: datetime.date
    id: Union[Unset, UUID] = UNSET
    source_count: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        updated_at = self.updated_at.isoformat()

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        source_count = self.source_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "updatedAt": updated_at,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if source_count is not UNSET:
            field_dict["sourceCount"] = source_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        updated_at = isoparse(d.pop("updatedAt")).date()

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        source_count = d.pop("sourceCount", UNSET)

        collection_dto = cls(
            name=name,
            updated_at=updated_at,
            id=id,
            source_count=source_count,
        )

        collection_dto.additional_properties = d
        return collection_dto

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
