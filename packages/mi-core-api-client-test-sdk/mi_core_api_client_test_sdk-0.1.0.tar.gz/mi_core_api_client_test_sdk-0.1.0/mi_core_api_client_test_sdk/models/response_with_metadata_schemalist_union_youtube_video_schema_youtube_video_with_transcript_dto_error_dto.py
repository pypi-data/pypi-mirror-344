from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.error_dto import ErrorDTO
    from ..models.metadata_schema import MetadataSchema
    from ..models.response_with_metadata_schemalist_union_youtube_video_schema_youtube_video_with_transcript_dto_error_dto_parameters import (
        ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTOParameters,
    )
    from ..models.youtube_video_schema import YoutubeVideoSchema
    from ..models.youtube_video_with_transcript_dto import YoutubeVideoWithTranscriptDTO


T = TypeVar("T", bound="ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO")


@_attrs_define
class ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO:
    """
    Attributes:
        metadata (MetadataSchema):
        parameters
            (ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTOParameters):
        response (list[Union['ErrorDTO', 'YoutubeVideoSchema', 'YoutubeVideoWithTranscriptDTO']]):
    """

    metadata: "MetadataSchema"
    parameters: "ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTOParameters"
    response: list[Union["ErrorDTO", "YoutubeVideoSchema", "YoutubeVideoWithTranscriptDTO"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.youtube_video_schema import YoutubeVideoSchema
        from ..models.youtube_video_with_transcript_dto import YoutubeVideoWithTranscriptDTO

        metadata = self.metadata.to_dict()

        parameters = self.parameters.to_dict()

        response = []
        for response_item_data in self.response:
            response_item: dict[str, Any]
            if isinstance(response_item_data, YoutubeVideoSchema):
                response_item = response_item_data.to_dict()
            elif isinstance(response_item_data, YoutubeVideoWithTranscriptDTO):
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
        from ..models.error_dto import ErrorDTO
        from ..models.metadata_schema import MetadataSchema
        from ..models.response_with_metadata_schemalist_union_youtube_video_schema_youtube_video_with_transcript_dto_error_dto_parameters import (
            ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTOParameters,
        )
        from ..models.youtube_video_schema import YoutubeVideoSchema
        from ..models.youtube_video_with_transcript_dto import YoutubeVideoWithTranscriptDTO

        d = dict(src_dict)
        metadata = MetadataSchema.from_dict(d.pop("metadata"))

        parameters = ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTOParameters.from_dict(
            d.pop("parameters")
        )

        response = []
        _response = d.pop("response")
        for response_item_data in _response:

            def _parse_response_item(
                data: object,
            ) -> Union["ErrorDTO", "YoutubeVideoSchema", "YoutubeVideoWithTranscriptDTO"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_item_type_0 = YoutubeVideoSchema.from_dict(data)

                    return response_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    response_item_type_1 = YoutubeVideoWithTranscriptDTO.from_dict(data)

                    return response_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                response_item_type_2 = ErrorDTO.from_dict(data)

                return response_item_type_2

            response_item = _parse_response_item(response_item_data)

            response.append(response_item)

        response_with_metadata_schemalist_union_youtube_video_schema_youtube_video_with_transcript_dto_error_dto = cls(
            metadata=metadata,
            parameters=parameters,
            response=response,
        )

        response_with_metadata_schemalist_union_youtube_video_schema_youtube_video_with_transcript_dto_error_dto.additional_properties = d
        return response_with_metadata_schemalist_union_youtube_video_schema_youtube_video_with_transcript_dto_error_dto

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
