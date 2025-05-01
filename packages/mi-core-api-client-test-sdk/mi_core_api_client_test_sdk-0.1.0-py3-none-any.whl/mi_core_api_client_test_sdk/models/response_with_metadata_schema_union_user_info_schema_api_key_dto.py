from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.api_key_dto import APIKeyDTO
    from ..models.metadata_schema import MetadataSchema
    from ..models.response_with_metadata_schema_union_user_info_schema_api_key_dto_parameters import (
        ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTOParameters,
    )
    from ..models.user_info_schema import UserInfoSchema


T = TypeVar("T", bound="ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO")


@_attrs_define
class ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters (ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTOParameters):
        response (Union['APIKeyDTO', 'UserInfoSchema']):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTOParameters"
    response: Union["APIKeyDTO", "UserInfoSchema"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_info_schema import UserInfoSchema

        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

        response: dict[str, Any]
        if isinstance(self.response, UserInfoSchema):
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
        from ..models.api_key_dto import APIKeyDTO
        from ..models.metadata_schema import MetadataSchema
        from ..models.response_with_metadata_schema_union_user_info_schema_api_key_dto_parameters import (
            ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTOParameters,
        )
        from ..models.user_info_schema import UserInfoSchema

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTOParameters.from_dict(d.pop("parameters"))

        def _parse_response(data: object) -> Union["APIKeyDTO", "UserInfoSchema"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_type_0 = UserInfoSchema.from_dict(data)

                return response_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_type_1 = APIKeyDTO.from_dict(data)

            return response_type_1

        response = _parse_response(d.pop("response"))

        response_with_metadata_schema_union_user_info_schema_api_key_dto = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schema_union_user_info_schema_api_key_dto.additional_properties = d
        return response_with_metadata_schema_union_user_info_schema_api_key_dto

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
