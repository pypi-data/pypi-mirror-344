from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.google_raw_serp_result_dto import GoogleRawSerpResultDTO
    from ..models.youtube_raw_serp_result_dto import YoutubeRawSerpResultDTO


T = TypeVar(
    "T", bound="ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTOResponse"
)


@_attrs_define
class ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTOResponse:
    """ """

    additional_properties: dict[str, list[Union["GoogleRawSerpResultDTO", "YoutubeRawSerpResultDTO"]]] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.google_raw_serp_result_dto import GoogleRawSerpResultDTO

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = []
            for additional_property_item_data in prop:
                additional_property_item: dict[str, Any]
                if isinstance(additional_property_item_data, GoogleRawSerpResultDTO):
                    additional_property_item = additional_property_item_data.to_dict()
                else:
                    additional_property_item = additional_property_item_data.to_dict()

                field_dict[prop_name].append(additional_property_item)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.google_raw_serp_result_dto import GoogleRawSerpResultDTO
        from ..models.youtube_raw_serp_result_dto import YoutubeRawSerpResultDTO

        d = dict(src_dict)
        response_with_metadata_schemadictstr_list_union_google_raw_serp_result_dto_youtube_raw_serp_result_dto_response = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = []
            _additional_property = prop_dict
            for additional_property_item_data in _additional_property:

                def _parse_additional_property_item(
                    data: object,
                ) -> Union["GoogleRawSerpResultDTO", "YoutubeRawSerpResultDTO"]:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        additional_property_item_type_0 = GoogleRawSerpResultDTO.from_dict(data)

                        return additional_property_item_type_0
                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_item_type_1 = YoutubeRawSerpResultDTO.from_dict(data)

                    return additional_property_item_type_1

                additional_property_item = _parse_additional_property_item(additional_property_item_data)

                additional_property.append(additional_property_item)

            additional_properties[prop_name] = additional_property

        response_with_metadata_schemadictstr_list_union_google_raw_serp_result_dto_youtube_raw_serp_result_dto_response.additional_properties = additional_properties
        return response_with_metadata_schemadictstr_list_union_google_raw_serp_result_dto_youtube_raw_serp_result_dto_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> list[Union["GoogleRawSerpResultDTO", "YoutubeRawSerpResultDTO"]]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: list[Union["GoogleRawSerpResultDTO", "YoutubeRawSerpResultDTO"]]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
