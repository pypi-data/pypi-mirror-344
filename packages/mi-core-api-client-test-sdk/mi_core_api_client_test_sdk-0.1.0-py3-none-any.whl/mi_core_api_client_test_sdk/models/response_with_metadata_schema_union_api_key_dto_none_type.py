from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.api_key_dto import APIKeyDTO
    from ..models.metadata_schema import MetadataSchema
    from ..models.response_with_metadata_schema_union_api_key_dto_none_type_parameters import (
        ResponseWithMetadataSchemaUnionAPIKeyDTONoneTypeParameters,
    )


T = TypeVar("T", bound="ResponseWithMetadataSchemaUnionAPIKeyDTONoneType")


@_attrs_define
class ResponseWithMetadataSchemaUnionAPIKeyDTONoneType:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters (ResponseWithMetadataSchemaUnionAPIKeyDTONoneTypeParameters):
        response (Union['APIKeyDTO', None]):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemaUnionAPIKeyDTONoneTypeParameters"
    response: Union["APIKeyDTO", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_key_dto import APIKeyDTO

        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

        response: Union[None, dict[str, Any]]
        if isinstance(self.response, APIKeyDTO):
            response = self.response.to_dict()
        else:
            response = self.response

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
        from ..models.api_key_dto import APIKeyDTO
        from ..models.metadata_schema import MetadataSchema
        from ..models.response_with_metadata_schema_union_api_key_dto_none_type_parameters import (
            ResponseWithMetadataSchemaUnionAPIKeyDTONoneTypeParameters,
        )

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = ResponseWithMetadataSchemaUnionAPIKeyDTONoneTypeParameters.from_dict(d.pop("parameters"))

        def _parse_response(data: object) -> Union["APIKeyDTO", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_type_0 = APIKeyDTO.from_dict(data)

                return response_type_0
            except:  # noqa: E722
                pass
            return cast(Union["APIKeyDTO", None], data)

        response = _parse_response(d.pop("response"))

        response_with_metadata_schema_union_api_key_dto_none_type = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schema_union_api_key_dto_none_type.additional_properties = d
        return response_with_metadata_schema_union_api_key_dto_none_type

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
