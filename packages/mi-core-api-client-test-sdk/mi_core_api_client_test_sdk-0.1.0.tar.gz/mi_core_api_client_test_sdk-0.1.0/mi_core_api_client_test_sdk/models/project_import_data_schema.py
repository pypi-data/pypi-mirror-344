from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_column_schema import CustomColumnSchema
    from ..models.report_base_schema_dto import ReportBaseSchemaDTO
    from ..models.source_import_schema import SourceImportSchema
    from ..models.workflow_import_schema import WorkflowImportSchema


T = TypeVar("T", bound="ProjectImportDataSchema")


@_attrs_define
class ProjectImportDataSchema:
    """
    Attributes:
        sources (Union[Unset, list['SourceImportSchema']]):
        reports (Union[Unset, list['ReportBaseSchemaDTO']]):
        custom_fields (Union[Unset, list['CustomColumnSchema']]):
        workflows (Union[Unset, list['WorkflowImportSchema']]):
    """

    sources: Union[Unset, list["SourceImportSchema"]] = UNSET
    reports: Union[Unset, list["ReportBaseSchemaDTO"]] = UNSET
    custom_fields: Union[Unset, list["CustomColumnSchema"]] = UNSET
    workflows: Union[Unset, list["WorkflowImportSchema"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sources: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sources, Unset):
            sources = []
            for sources_item_data in self.sources:
                sources_item = sources_item_data.to_dict()
                sources.append(sources_item)

        reports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.reports, Unset):
            reports = []
            for reports_item_data in self.reports:
                reports_item = reports_item_data.to_dict()
                reports.append(reports_item)

        custom_fields: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = []
            for custom_fields_item_data in self.custom_fields:
                custom_fields_item = custom_fields_item_data.to_dict()
                custom_fields.append(custom_fields_item)

        workflows: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.workflows, Unset):
            workflows = []
            for workflows_item_data in self.workflows:
                workflows_item = workflows_item_data.to_dict()
                workflows.append(workflows_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sources is not UNSET:
            field_dict["sources"] = sources
        if reports is not UNSET:
            field_dict["reports"] = reports
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if workflows is not UNSET:
            field_dict["workflows"] = workflows

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_column_schema import CustomColumnSchema
        from ..models.report_base_schema_dto import ReportBaseSchemaDTO
        from ..models.source_import_schema import SourceImportSchema
        from ..models.workflow_import_schema import WorkflowImportSchema

        d = dict(src_dict)
        sources = []
        _sources = d.pop("sources", UNSET)
        for sources_item_data in _sources or []:
            sources_item = SourceImportSchema.from_dict(sources_item_data)

            sources.append(sources_item)

        reports = []
        _reports = d.pop("reports", UNSET)
        for reports_item_data in _reports or []:
            reports_item = ReportBaseSchemaDTO.from_dict(reports_item_data)

            reports.append(reports_item)

        custom_fields = []
        _custom_fields = d.pop("customFields", UNSET)
        for custom_fields_item_data in _custom_fields or []:
            custom_fields_item = CustomColumnSchema.from_dict(custom_fields_item_data)

            custom_fields.append(custom_fields_item)

        workflows = []
        _workflows = d.pop("workflows", UNSET)
        for workflows_item_data in _workflows or []:
            workflows_item = WorkflowImportSchema.from_dict(workflows_item_data)

            workflows.append(workflows_item)

        project_import_data_schema = cls(
            sources=sources,
            reports=reports,
            custom_fields=custom_fields,
            workflows=workflows,
        )

        project_import_data_schema.additional_properties = d
        return project_import_data_schema

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
