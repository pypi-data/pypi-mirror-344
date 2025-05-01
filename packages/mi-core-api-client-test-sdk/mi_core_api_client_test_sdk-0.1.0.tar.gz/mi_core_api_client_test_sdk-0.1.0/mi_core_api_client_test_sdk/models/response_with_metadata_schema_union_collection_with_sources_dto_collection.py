from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.collection import Collection
    from ..models.collection_with_sources_dto import CollectionWithSourcesDTO
    from ..models.metadata_schema import MetadataSchema
    from ..models.response_with_metadata_schema_union_collection_with_sources_dto_collection_parameters import (
        ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollectionParameters,
    )


T = TypeVar("T", bound="ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection")


@_attrs_define
class ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters (ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollectionParameters):
        response (Union['Collection', 'CollectionWithSourcesDTO']):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollectionParameters"
    response: Union["Collection", "CollectionWithSourcesDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.collection_with_sources_dto import CollectionWithSourcesDTO

        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

        response: dict[str, Any]
        if isinstance(self.response, CollectionWithSourcesDTO):
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
        from ..models.collection import Collection
        from ..models.collection_with_sources_dto import CollectionWithSourcesDTO
        from ..models.metadata_schema import MetadataSchema
        from ..models.response_with_metadata_schema_union_collection_with_sources_dto_collection_parameters import (
            ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollectionParameters,
        )

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollectionParameters.from_dict(
            d.pop("parameters")
        )

        def _parse_response(data: object) -> Union["Collection", "CollectionWithSourcesDTO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_type_0 = CollectionWithSourcesDTO.from_dict(data)

                return response_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_type_1 = Collection.from_dict(data)

            return response_type_1

        response = _parse_response(d.pop("response"))

        response_with_metadata_schema_union_collection_with_sources_dto_collection = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schema_union_collection_with_sources_dto_collection.additional_properties = d
        return response_with_metadata_schema_union_collection_with_sources_dto_collection

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
