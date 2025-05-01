from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.gateway_error_dto import GatewayErrorDTO
    from ..models.gateway_subreddit_info_with_last_post_dto import GatewaySubredditInfoWithLastPostDTO
    from ..models.metadata_schema import MetadataSchema
    from ..models.response_with_metadata_schemalist_union_gateway_subreddit_info_with_last_post_dto_gateway_error_dto_parameters import (
        ResponseWithMetadataSchemalistUnionGatewaySubredditInfoWithLastPostDTOGatewayErrorDTOParameters,
    )


T = TypeVar("T", bound="ResponseWithMetadataSchemalistUnionGatewaySubredditInfoWithLastPostDTOGatewayErrorDTO")


@_attrs_define
class ResponseWithMetadataSchemalistUnionGatewaySubredditInfoWithLastPostDTOGatewayErrorDTO:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters (ResponseWithMetadataSchemalistUnionGatewaySubredditInfoWithLastPostDTOGatewayErrorDTOParameters):
        response (list[Union['GatewayErrorDTO', 'GatewaySubredditInfoWithLastPostDTO']]):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemalistUnionGatewaySubredditInfoWithLastPostDTOGatewayErrorDTOParameters"
    response: list[Union["GatewayErrorDTO", "GatewaySubredditInfoWithLastPostDTO"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.gateway_subreddit_info_with_last_post_dto import GatewaySubredditInfoWithLastPostDTO

        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

        response = []
        for response_item_data in self.response:
            response_item: dict[str, Any]
            if isinstance(response_item_data, GatewaySubredditInfoWithLastPostDTO):
                response_item = response_item_data.to_dict()
            else:
                response_item = response_item_data.to_dict()

            response.append(response_item)

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
        from ..models.gateway_error_dto import GatewayErrorDTO
        from ..models.gateway_subreddit_info_with_last_post_dto import GatewaySubredditInfoWithLastPostDTO
        from ..models.metadata_schema import MetadataSchema
        from ..models.response_with_metadata_schemalist_union_gateway_subreddit_info_with_last_post_dto_gateway_error_dto_parameters import (
            ResponseWithMetadataSchemalistUnionGatewaySubredditInfoWithLastPostDTOGatewayErrorDTOParameters,
        )

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = (
            ResponseWithMetadataSchemalistUnionGatewaySubredditInfoWithLastPostDTOGatewayErrorDTOParameters.from_dict(
                d.pop("parameters")
            )
        )

        response = []
        _response = d.pop("response")
        for response_item_data in _response:

            def _parse_response_item(data: object) -> Union["GatewayErrorDTO", "GatewaySubredditInfoWithLastPostDTO"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_item_type_0 = GatewaySubredditInfoWithLastPostDTO.from_dict(data)

                    return response_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_item_type_1 = GatewayErrorDTO.from_dict(data)

                return response_item_type_1

            response_item = _parse_response_item(response_item_data)

            response.append(response_item)

        response_with_metadata_schemalist_union_gateway_subreddit_info_with_last_post_dto_gateway_error_dto = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schemalist_union_gateway_subreddit_info_with_last_post_dto_gateway_error_dto.additional_properties = d
        return response_with_metadata_schemalist_union_gateway_subreddit_info_with_last_post_dto_gateway_error_dto

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
