from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metadata_schema import MetadataSchema
    from ..models.paginated_response_prompt_info_schema import PaginatedResponsePromptInfoSchema
    from ..models.response_with_metadata_schema_paginated_response_prompt_info_schema_parameters import (
        ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchemaParameters,
    )


T = TypeVar("T", bound="ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema")


@_attrs_define
class ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters (ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchemaParameters):
        response (PaginatedResponsePromptInfoSchema):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchemaParameters"
    response: "PaginatedResponsePromptInfoSchema"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

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
        from ..models.paginated_response_prompt_info_schema import PaginatedResponsePromptInfoSchema
        from ..models.response_with_metadata_schema_paginated_response_prompt_info_schema_parameters import (
            ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchemaParameters,
        )

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchemaParameters.from_dict(
            d.pop("parameters")
        )

        response = PaginatedResponsePromptInfoSchema.from_dict(d.pop("response"))

        response_with_metadata_schema_paginated_response_prompt_info_schema = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schema_paginated_response_prompt_info_schema.additional_properties = d
        return response_with_metadata_schema_paginated_response_prompt_info_schema

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
