from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metadata_schema import MetadataSchema
    from ..models.project_base_schema import ProjectBaseSchema
    from ..models.project_with_all_relations_dto import ProjectWithAllRelationsDTO
    from ..models.project_with_reports_dto import ProjectWithReportsDTO
    from ..models.project_with_sources_dto import ProjectWithSourcesDTO
    from ..models.response_with_metadata_schema_union_project_with_sources_dto_project_with_reports_dto_project_with_all_relations_dto_project_base_schema_parameters import (
        ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchemaParameters,
    )


T = TypeVar(
    "T",
    bound="ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema",
)


@_attrs_define
class ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters (ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOP
            rojectBaseSchemaParameters):
        response (Union['ProjectBaseSchema', 'ProjectWithAllRelationsDTO', 'ProjectWithReportsDTO',
            'ProjectWithSourcesDTO']):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchemaParameters"
    response: Union["ProjectBaseSchema", "ProjectWithAllRelationsDTO", "ProjectWithReportsDTO", "ProjectWithSourcesDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_with_all_relations_dto import ProjectWithAllRelationsDTO
        from ..models.project_with_reports_dto import ProjectWithReportsDTO
        from ..models.project_with_sources_dto import ProjectWithSourcesDTO

        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

        response: dict[str, Any]
        if isinstance(self.response, ProjectWithSourcesDTO):
            response = self.response.to_dict()
        elif isinstance(self.response, ProjectWithReportsDTO):
            response = self.response.to_dict()
        elif isinstance(self.response, ProjectWithAllRelationsDTO):
            response = self.response.to_dict()
        else:
            response = self.response.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
                "parameters": parameters,
                "response": response,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_schema import MetadataSchema
        from ..models.project_base_schema import ProjectBaseSchema
        from ..models.project_with_all_relations_dto import ProjectWithAllRelationsDTO
        from ..models.project_with_reports_dto import ProjectWithReportsDTO
        from ..models.project_with_sources_dto import ProjectWithSourcesDTO
        from ..models.response_with_metadata_schema_union_project_with_sources_dto_project_with_reports_dto_project_with_all_relations_dto_project_base_schema_parameters import (
            ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchemaParameters,
        )

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchemaParameters.from_dict(
            d.pop("parameters")
        )

        def _parse_response(
            data: object,
        ) -> Union["ProjectBaseSchema", "ProjectWithAllRelationsDTO", "ProjectWithReportsDTO", "ProjectWithSourcesDTO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_type_0 = ProjectWithSourcesDTO.from_dict(data)

                return response_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_type_1 = ProjectWithReportsDTO.from_dict(data)

                return response_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_type_2 = ProjectWithAllRelationsDTO.from_dict(data)

                return response_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_type_3 = ProjectBaseSchema.from_dict(data)

            return response_type_3

        response = _parse_response(d.pop("response"))

        response_with_metadata_schema_union_project_with_sources_dto_project_with_reports_dto_project_with_all_relations_dto_project_base_schema = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schema_union_project_with_sources_dto_project_with_reports_dto_project_with_all_relations_dto_project_base_schema.additional_properties = d
        return response_with_metadata_schema_union_project_with_sources_dto_project_with_reports_dto_project_with_all_relations_dto_project_base_schema

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
