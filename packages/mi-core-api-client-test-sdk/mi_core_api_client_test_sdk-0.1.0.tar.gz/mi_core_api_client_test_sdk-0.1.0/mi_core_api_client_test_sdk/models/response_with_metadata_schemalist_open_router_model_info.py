from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metadata_schema import MetadataSchema
    from ..models.open_router_model_info import OpenRouterModelInfo
    from ..models.response_with_metadata_schemalist_open_router_model_info_parameters import (
        ResponseWithMetadataSchemalistOpenRouterModelInfoParameters,
    )


T = TypeVar("T", bound="ResponseWithMetadataSchemalistOpenRouterModelInfo")


@_attrs_define
class ResponseWithMetadataSchemalistOpenRouterModelInfo:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters (ResponseWithMetadataSchemalistOpenRouterModelInfoParameters):
        response (list['OpenRouterModelInfo']):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemalistOpenRouterModelInfoParameters"
    response: list["OpenRouterModelInfo"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

        response = []
        for response_item_data in self.response:
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
        from ..models.metadata_schema import MetadataSchema
        from ..models.open_router_model_info import OpenRouterModelInfo
        from ..models.response_with_metadata_schemalist_open_router_model_info_parameters import (
            ResponseWithMetadataSchemalistOpenRouterModelInfoParameters,
        )

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = ResponseWithMetadataSchemalistOpenRouterModelInfoParameters.from_dict(d.pop("parameters"))

        response = []
        _response = d.pop("response")
        for response_item_data in _response:
            response_item = OpenRouterModelInfo.from_dict(response_item_data)

            response.append(response_item)

        response_with_metadata_schemalist_open_router_model_info = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schemalist_open_router_model_info.additional_properties = d
        return response_with_metadata_schemalist_open_router_model_info

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
