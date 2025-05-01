from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectCreateRequestSchema")


@_attrs_define
class ProjectCreateRequestSchema:
    """
    Attributes:
        name (str):
        description (str):
        source_ids (Union[Unset, list[UUID]]): List of source IDs to attach to project
        collection_ids (Union[Unset, list[UUID]]): List of collection IDs to attach to project
    """

    name: str
    description: str
    source_ids: Union[Unset, list[UUID]] = UNSET
    collection_ids: Union[Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        source_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.source_ids, Unset):
            source_ids = []
            for source_ids_item_data in self.source_ids:
                source_ids_item = str(source_ids_item_data)
                source_ids.append(source_ids_item)

        collection_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.collection_ids, Unset):
            collection_ids = []
            for collection_ids_item_data in self.collection_ids:
                collection_ids_item = str(collection_ids_item_data)
                collection_ids.append(collection_ids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )
        if source_ids is not UNSET:
            field_dict["source_ids"] = source_ids
        if collection_ids is not UNSET:
            field_dict["collection_ids"] = collection_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        source_ids = []
        _source_ids = d.pop("source_ids", UNSET)
        for source_ids_item_data in _source_ids or []:
            source_ids_item = UUID(source_ids_item_data)

            source_ids.append(source_ids_item)

        collection_ids = []
        _collection_ids = d.pop("collection_ids", UNSET)
        for collection_ids_item_data in _collection_ids or []:
            collection_ids_item = UUID(collection_ids_item_data)

            collection_ids.append(collection_ids_item)

        project_create_request_schema = cls(
            name=name,
            description=description,
            source_ids=source_ids,
            collection_ids=collection_ids,
        )

        project_create_request_schema.additional_properties = d
        return project_create_request_schema

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
