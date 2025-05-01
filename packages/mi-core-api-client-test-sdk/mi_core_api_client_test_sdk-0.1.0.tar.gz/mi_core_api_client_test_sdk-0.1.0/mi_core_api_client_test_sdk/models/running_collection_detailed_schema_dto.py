from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.graph_extraction_dto import GraphExtractionDTO
    from ..models.project_create_result_schema import ProjectCreateResultSchema
    from ..models.running_collection_summary import RunningCollectionSummary


T = TypeVar("T", bound="RunningCollectionDetailedSchemaDTO")


@_attrs_define
class RunningCollectionDetailedSchemaDTO:
    """
    Attributes:
        report_id (UUID):
        is_extracted_entities (bool):
        is_summary_per_source (bool):
        is_overall_summary (bool):
        status (JobStatus): Enumeration class representing job statuses.

            Attributes:
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
        project (ProjectCreateResultSchema):
        entities (Union['GraphExtractionDTO', None]):
        summary (Union['RunningCollectionSummary', None]):
        id (Union[Unset, UUID]):
    """

    report_id: UUID
    is_extracted_entities: bool
    is_summary_per_source: bool
    is_overall_summary: bool
    status: JobStatus
    project: "ProjectCreateResultSchema"
    entities: Union["GraphExtractionDTO", None]
    summary: Union["RunningCollectionSummary", None]
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.graph_extraction_dto import GraphExtractionDTO
        from ..models.running_collection_summary import RunningCollectionSummary

        report_id = str(self.report_id)

        is_extracted_entities = self.is_extracted_entities

        is_summary_per_source = self.is_summary_per_source

        is_overall_summary = self.is_overall_summary

        status = self.status.value

        project = self.project.to_dict()

        entities: Union[None, dict[str, Any]]
        if isinstance(self.entities, GraphExtractionDTO):
            entities = self.entities.to_dict()
        else:
            entities = self.entities

        summary: Union[None, dict[str, Any]]
        if isinstance(self.summary, RunningCollectionSummary):
            summary = self.summary.to_dict()
        else:
            summary = self.summary

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reportId": report_id,
                "isExtractedEntities": is_extracted_entities,
                "isSummaryPerSource": is_summary_per_source,
                "isOverallSummary": is_overall_summary,
                "status": status,
                "project": project,
                "entities": entities,
                "summary": summary,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.graph_extraction_dto import GraphExtractionDTO
        from ..models.project_create_result_schema import ProjectCreateResultSchema
        from ..models.running_collection_summary import RunningCollectionSummary

        d = dict(src_dict)
        report_id = UUID(d.pop("reportId"))

        is_extracted_entities = d.pop("isExtractedEntities")

        is_summary_per_source = d.pop("isSummaryPerSource")

        is_overall_summary = d.pop("isOverallSummary")

        status = JobStatus(d.pop("status"))

        project = ProjectCreateResultSchema.from_dict(d.pop("project"))

        def _parse_entities(data: object) -> Union["GraphExtractionDTO", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                entities_type_0 = GraphExtractionDTO.from_dict(data)

                return entities_type_0
            except:  # noqa: E722
                pass
            return cast(Union["GraphExtractionDTO", None], data)

        entities = _parse_entities(d.pop("entities"))

        def _parse_summary(data: object) -> Union["RunningCollectionSummary", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_0 = RunningCollectionSummary.from_dict(data)

                return summary_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunningCollectionSummary", None], data)

        summary = _parse_summary(d.pop("summary"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        running_collection_detailed_schema_dto = cls(
            report_id=report_id,
            is_extracted_entities=is_extracted_entities,
            is_summary_per_source=is_summary_per_source,
            is_overall_summary=is_overall_summary,
            status=status,
            project=project,
            entities=entities,
            summary=summary,
            id=id,
        )

        running_collection_detailed_schema_dto.additional_properties = d
        return running_collection_detailed_schema_dto

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
