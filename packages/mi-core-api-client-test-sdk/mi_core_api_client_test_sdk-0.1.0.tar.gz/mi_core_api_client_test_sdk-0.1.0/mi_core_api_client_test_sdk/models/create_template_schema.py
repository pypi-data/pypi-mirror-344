from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateTemplateSchema")


@_attrs_define
class CreateTemplateSchema:
    """
    Attributes:
        name (str):
        project_id (UUID):
        with_reports (Union[Unset, bool]):  Default: False.
        with_custom_fields (Union[Unset, bool]):  Default: False.
        with_workflows (Union[Unset, bool]):  Default: False.
        with_sources (Union[Unset, bool]):  Default: False.
    """

    name: str
    project_id: UUID
    with_reports: Union[Unset, bool] = False
    with_custom_fields: Union[Unset, bool] = False
    with_workflows: Union[Unset, bool] = False
    with_sources: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        project_id = str(self.project_id)

        with_reports = self.with_reports

        with_custom_fields = self.with_custom_fields

        with_workflows = self.with_workflows

        with_sources = self.with_sources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "project_id": project_id,
            }
        )
        if with_reports is not UNSET:
            field_dict["with_reports"] = with_reports
        if with_custom_fields is not UNSET:
            field_dict["with_custom_fields"] = with_custom_fields
        if with_workflows is not UNSET:
            field_dict["with_workflows"] = with_workflows
        if with_sources is not UNSET:
            field_dict["with_sources"] = with_sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        project_id = UUID(d.pop("project_id"))

        with_reports = d.pop("with_reports", UNSET)

        with_custom_fields = d.pop("with_custom_fields", UNSET)

        with_workflows = d.pop("with_workflows", UNSET)

        with_sources = d.pop("with_sources", UNSET)

        create_template_schema = cls(
            name=name,
            project_id=project_id,
            with_reports=with_reports,
            with_custom_fields=with_custom_fields,
            with_workflows=with_workflows,
            with_sources=with_sources,
        )

        create_template_schema.additional_properties = d
        return create_template_schema

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
